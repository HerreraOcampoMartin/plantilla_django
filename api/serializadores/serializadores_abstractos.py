from rest_framework import serializers
from django.db.models import ForeignKey, ManyToManyField


class BaseEliminacionLogicaSerializer(serializers.ModelSerializer):
    """
    Serializer base que aplica validación para prevenir referencias a entidades
    que han sido marcadas como eliminadas lógicamente (eliminado=True).
    """

    def validate(self, data):
        """
        Sobrescribe el validate() para revisar todas las FK y M2M.
        """
        # Obtenemos el modelo asociado a este Serializer a través de Meta
        model = self.Meta.model

        for field in model._meta.get_fields():
            field_name = field.name

            # --- VALIDACIÓN M:N ---
            # El campo ManyToManyField viene como una lista de objetos en 'data'
            if isinstance(field, ManyToManyField) and field_name in data:
                referencias = data[field_name]
                RelatedModel = field.related_model

                # Solo validamos si el modelo relacionado soporta eliminación lógica
                if hasattr(RelatedModel, 'eliminado'):
                    ids = [ref.pk for ref in referencias]

                    # Contamos cuántos de los IDs existen y NO están eliminados
                    activos_count = RelatedModel.objects.filter(pk__in=ids, eliminado=False).count()

                    if activos_count != len(ids):
                        raise serializers.ValidationError({
                            field_name: "La lista contiene referencias a elementos eliminados o inexistentes."
                        })

            # --- VALIDACIÓN FK (1:N) ---
            # El campo ForeignKey viene como un objeto completo en 'data' (DRF ya lo buscó)
            elif isinstance(field, ForeignKey) and field_name in data:
                objeto_referenciado = data[field_name]

                # Solo validamos si el objeto referenciado soporta eliminación lógica
                if hasattr(objeto_referenciado, 'eliminado'):
                    # Comprobamos si el objeto existe Y está marcado como eliminado=True
                    if objeto_referenciado.eliminado:
                        raise serializers.ValidationError({
                            field_name: f"El objeto referenciado por '{field_name}' ya no existe."
                        })

        return super().validate(data)  # Llama a las validaciones de la clase base
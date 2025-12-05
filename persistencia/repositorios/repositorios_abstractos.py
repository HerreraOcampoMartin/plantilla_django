from casos_de_uso.interfaces.interfaces import IRepository
from typing import TypeVar, Generic, Optional, List
from django.db import models
from core.modelos.modelos_abstractos import ModeloEliminacionLogica

T = TypeVar('T', bound=models.Model)

class RepositorioBaseDjangoORM(IRepository[T], Generic[T]):
    """Implementación base genérica para el ORM de Django."""

    def __init__(self, model: type[models.Model]):
        self.model = model

    def guardar(self, entidad: T):
        entidad.save()

    def crear_desde_dict(self, data: dict) -> Optional[T]:
        m2m_data = {}

        # 1. Identificar y separar todos los campos ManyToMany (M:N)
        # Recorremos los campos del modelo
        for field in self.model._meta.many_to_many:
            field_name = field.name  # El nombre del campo (ej: 'filtros')

            # Verificamos si ese campo (ej: 'filtros') está en los datos de entrada
            if field_name in data:
                # Guardamos la lista de IDs de la relación y lo eliminamos del diccionario de creación
                m2m_data[field_name] = data.pop(field_name)

        nueva_instancia = self.model.objects.create(**data)

        if m2m_data:
            for field_name, ids in m2m_data.items():
                # Accedemos al manager M:N de la instancia (ej: nueva_instancia.filtros)
                # y usamos .set() para asignar los IDs.
                getattr(nueva_instancia, field_name).set(ids)

        return nueva_instancia

    def obtener_por_id(self, entidad_id: int) -> Optional[T]:
        try:
            return self.model.objects.get(pk=entidad_id)
        except self.model.DoesNotExist:
            return None

    def obtener_todos(self) -> List[T]:
        return list(self.model.objects.all())

    def eliminar_por_id(self, entidad_id: int):
        self.model.objects.get(pk=entidad_id).delete()


# ============================================
# = GESTIÓN DE ELIMINACIÓN LÓGICA
# ============================================
T_EliminacionLogica = TypeVar('T_EliminacionLogica', bound=ModeloEliminacionLogica)

class RepositorioBaseEliminacionLogicaDjangoORM(RepositorioBaseDjangoORM[T_EliminacionLogica], Generic[T_EliminacionLogica]):

    def guardar(self, entidad: T):
        if not entidad.pk:
            entidad.eliminado = False

        super().guardar(entidad)

    def crear_desde_dict(self, data: dict) -> Optional[T]:
        if 'eliminado' in data:
            data['eliminado'] = False

        return super().crear_desde_dict(data)

    def obtener_por_id(self, entidad_id: int) -> Optional[T]:
        try:
            return self.model.objects.filter(eliminado=False).get(pk=entidad_id)
        except self.model.DoesNotExist:
            return None

    def obtener_todos(self) -> List[T]:
        return list(self.model.objects.filter(eliminado=False).all())

    def eliminar_por_id(self, entidad_id: int):
        try:
            instancia = self.model.objects.get(pk=entidad_id, eliminado=False)
            instancia.eliminado = True
            instancia.save()

            # Opcional: Si quieres ejecutar señales de pre_delete/post_delete,
            # puedes llamar a instancia.delete() pero DEBES sobrescribir
            # el método delete() del modelo para que solo haga la eliminación lógica.

        except self.model.DoesNotExist:
            pass


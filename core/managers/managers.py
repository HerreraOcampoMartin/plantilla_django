from django.db import models

# =============================
# = PARA MODELO ORDENABLE
# =============================
class OrdenableQuerySet(models.QuerySet):
    def all(self):
        # Aplica el ordenamiento por defecto a todas las consultas QuerySet
        return super().all().order_by('orden')

class OrdenableManager(models.Manager):
    # Usa el QuerySet personalizado
    def get_queryset(self):
        return OrdenableQuerySet(self.model, using=self._db)
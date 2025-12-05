from django.db import models
from core.managers.managers import OrdenableManager

class ModeloEliminacionLogica(models.Model):
    """ Modelo base que ofrece la posibilidad de hacer eliminaciones lógicas """
    eliminado = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ModeloOrdenable(models.Model):
    """ Modelo base que ofrece la posibilidad de hacer modelos ordenables """
    orden = models.IntegerField()

    # Aplica el manager al modelo abstracto
    objects = OrdenableManager()

    class Meta:
        abstract = True

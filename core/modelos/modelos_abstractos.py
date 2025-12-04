from django.db import models

class ModeloEliminacionLogica(models.Model):
    """ Modelo base que ofrece la posibilidad de hacer eliminaciones lógicas """
    eliminado = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ModeloOrdenable(models.Model):
    orden = models.IntegerField()

    class Meta:
        abstract = True

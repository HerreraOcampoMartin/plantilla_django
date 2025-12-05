"""
from persistencia.repositorios.repositorios_abstractos import RepositorioBaseDjangoORM

class ModeloDeEjemploRepositorio(RepositorioBaseDjangoORM[ModeloDeEjemplo]):
    def __init__(self):
        super().__init__(model=ModeloDeEjemplo)
"""


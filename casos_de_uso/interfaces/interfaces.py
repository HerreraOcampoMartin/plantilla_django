from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List
from django.db import models

T = TypeVar('T', bound=models.Model)

class IRepository(ABC, Generic[T]):
    """Interfaz Genérica de Repositorio para operaciones básicas."""

    @abstractmethod
    def guardar(self, entidad: dict):
        """Guarda o actualiza la entidad."""
        pass

    @abstractmethod
    def crear_desde_dict(self, entidad: dict) -> Optional[T]:
        """Guarda o actualiza la entidad."""
        pass

    @abstractmethod
    def obtener_por_id(self, entidad_id: int) -> Optional[T]:
        """Obtiene una entidad por su ID."""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[T]:
        """Obtiene todas las entidades de este tipo."""
        pass

    @abstractmethod
    def eliminar_por_id(self, entidad_id: int):
        """Elimina una entidad por su ID."""
        pass


from rest_framework import viewsets, status
from rest_framework.response import Response
from typing import TypeVar, Type
from django.db import models
from rest_framework.exceptions import NotFound
from rest_framework.serializers import Serializer
from casos_de_uso.interfaces.interfaces import IRepository

TModel = TypeVar('TModel', bound=models.Model) # TODO: cambiar a modelo con eliminación lógica
TRepository = TypeVar('TRepository', bound='IRepository')


class ControladorBase(viewsets.ModelViewSet):
    model: Type[TModel] = None
    serializer_class: Type[Serializer] = None
    repository_class: Type[TRepository] = None
    serializer_write_class: Type[Serializer] = None

    repository: IRepository = None

    def get_serializer_class(self):
        # Usamos el serializer de escritura para las acciones de modificación
        if self.action in ['create', 'partial_update'] and self.serializer_write_class is not None:
            return self.serializer_write_class

        return self.serializer_class

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.repository_class is None:
            # Lanzar una excepción si no se define la clase requerida
            raise NotImplementedError("La clase 'repository_class' debe ser definida e implementar IRepository.")

        # Inicializa el repositorio. Gracias a 'repository_class: Type[TRepository]'
        # y TRepository acotado a IRepository, sabemos que tendrá los métodos correctos.
        self.repository = self.repository_class()

    # =======================================================
    # 1. GET (LIST)
    # =======================================================
    def list(self, request, *args, **kwargs):
        """Usa repository.obtener_todos()"""
        queryset = self.repository.obtener_todos()

        # ... (código de paginación y serialización) ...
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # =======================================================
    # 2. GET (por ID) (RETRIEVE)
    # =======================================================
    def get_object(self):
        """Usa repository.obtener_por_id(pk)"""
        pk = self.kwargs.get('pk')
        if pk is None:
            raise NotFound("ID (pk) no proporcionado.")

        try:
            obj = self.repository.obtener_por_id(pk)
        except Exception:
            obj = None

        if obj is None:
            raise NotFound(detail=f"No se encontró {self.model.__name__} con ID {pk}.")

        self.check_object_permissions(self.request, obj)
        return obj

    # =======================================================
    # 3. POST
    # =======================================================
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nueva_instancia = self.repository.crear_desde_dict(serializer.validated_data)

        # El serializer tiene guardado los datos pre-guardado, para devolver el ID y esas cuestiones, necesito
        # serializar el nuevo objeto que fue creado
        serializer = self.get_serializer(nueva_instancia)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # =======================================================
    # 4. PATCH (PARTIAL UPDATE)
    # =======================================================
    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 1. Aplicar cambios al objeto en memoria
        updated_instance = serializer.save()

        # 2. Persistir usando el Repositorio
        self.repository.guardar(updated_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # =======================================================
    # 5. ELIMINAR (DESTROY)
    # =======================================================
    def destroy(self, request, *args, **kwargs):
        """Usa repository.eliminar_por_id(pk)."""
        pk = self.kwargs.get('pk')
        if pk is None:
            raise NotFound("ID no proporcionado para eliminación.")

        self.repository.eliminar_por_id(pk)

        return Response(status=status.HTTP_204_NO_CONTENT)

# from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt  # Чтобы post, put, patch, delete не требовали csrf токена
# (небезопасно)
from apps.db_train_alternative.models import Author
from .serializers import AuthorSerializer, AuthorModelSerializer

from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                                   DestroyModelMixin)
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions


class AuthorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, pk=None):
        if pk is not None:
            try:
                author = Author.objects.get(pk=pk)
                serializer = AuthorModelSerializer(author)
                return Response(serializer.data)
            except Author.DoesNotExist:
                return Response({"message": "Автор не найден"}, status=status.HTTP_404_NOT_FOUND)
        else:
            authors = Author.objects.all()
            serializer = AuthorModelSerializer(authors, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AuthorModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response({"message": "Автор не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorModelSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response({"message": "Автор не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorModelSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response({"message": "Автор не найден"}, status=status.HTTP_404_NOT_FOUND)

        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomPermission(permissions.BasePermission):
    """
    Пользователи могут выполнять различные действия в зависимости от их роли.
    """

    def has_permission(self, request, view):
        # Разрешаем только GET запросы для неаутентифицированных пользователей
        if request.method == 'GET' and not request.user.is_authenticated:
            return True

        # Разрешаем GET и POST запросы для аутентифицированных пользователей
        if request.method in ['GET', 'POST'] and request.user.is_authenticated:
            return True

        # Разрешаем все действия для администраторов
        if request.user.is_superuser:
            return True

        # Во всех остальных случаях возвращаем False
        return False


class AuthorGenericAPIView(GenericAPIView, RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                           DestroyModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer

    # Переопределяем атрибут permission_classes для указания нашего собственного разрешения
    permission_classes = [CustomPermission]

    def get(self, request, *args, **kwargs):
        if kwargs.get(self.lookup_field):  # если был передан id или pk
            # возвращаем один объект
            try:
                return self.retrieve(request, *args, **kwargs)
            except Http404:
                return Response({'message': 'Ну нет такого автора'}, status=status.HTTP_404_NOT_FOUND)
        # Иначе возвращаем список объектов
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AuthorPagination(PageNumberPagination):
    page_size = 5  # количество объектов на странице
    page_size_query_param = 'page_size'  # параметр запроса для настройки количества объектов на странице
    max_page_size = 1000  # максимальное количество объектов на странице


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'email']
    search_fields = ['email']  # Поля, по которым будет выполняться поиск
    ordering_fields = ['name', 'email']  # Поля, по которым можно сортировать
    pagination_class = AuthorPagination


def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__contains=name)
        return queryset

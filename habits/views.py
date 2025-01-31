from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from src.utils import get_queryset_for_owner
from users.permissions import IsOwner

from .models import Habit, Place
from .paginators import HabitPaginator
from .serializers import PlaceSerializer, HabitSerializer


# Create your views here.
class HabitListCreateAPIView(generics.ListCreateAPIView):
    """
    Дженерик для отображения списка и создания нового объекта Habit:
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        """
        Подбор списка объектов в зависимости от статуса пользователя
        """
        return get_queryset_for_owner(self.request.user, self.queryset)

    def perform_create(self, serializer):
        """
        Сохранение владельца при создании объекта
        """
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Дженерик для просмотра, редактирования и удаления объекта Habit:
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner | IsAdminUser]


class PlaceListCreateAPIView(generics.ListCreateAPIView):
    """
    Дженерик для отображения списка и создания нового объекта Place:
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def perform_create(self, serializer):
        """
        Сохранение владельца при создании объекта
        """
        place = serializer.save()
        place.owner = self.request.user
        place.save()


class PlaceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Дженерик для просмотра, редактирования и удаления объекта Place:
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes =[IsOwner | IsAdminUser]

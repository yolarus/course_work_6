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
    Дженерик для отображения списка и создания нового объекта Habit
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
        Сохранение владельца при создании объекта и форматирование дней недели
        """
        habit = serializer.save()
        habit.owner = self.request.user
        habit.frequency = [day.lower().capitalize() for day in habit.frequency]
        habit.save()


class HabitListPublicAPIView(generics.ListAPIView):
    """
    Дженерик для отображения списка публичных объектов Habit:
    """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Дженерик для просмотра, редактирования и удаления объекта Habit
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner | IsAdminUser]

    def perform_update(self, serializer):
        """
        Форматирование дней недели
        """
        habit = serializer.save()
        habit.frequency = [day.lower().capitalize() for day in habit.frequency]
        habit.save()


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

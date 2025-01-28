from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsCurrentUser
from .serializers import NewUserSerializer, UserDetailSerializer, UserSerializer


# Create your views here.
class UserListCreateAPIView(generics.ListCreateAPIView):
    """
    Дженерик для отображения списка и создания нового объекта User:
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Выдача разрешений в зависимости от статуса пользователя
        """
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        """
        Подбор сериализатора в зависимости от действий на странице
        """
        if self.request.method == "POST":
            return NewUserSerializer
        return UserSerializer

    def perform_create(self, serializer):
        """
        Сохранение пароля и активация учетной записи при создании
        """
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Дженерик для просмотра, редактирования и удаления объекта User:
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_class(self):
        """
        Подбор сериализатора в зависимости от статуса пользователя
        """
        if self.request.user.is_superuser or self.request.user == self.get_object():
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Выдача разрешений в зависимости от статуса пользователя
        """
        if self.request.method in ["PATCH", "PUT", "DELETE"]:
            self.permission_classes = [IsCurrentUser | IsAdminUser]
        return super().get_permissions()


class MyToken(TokenObtainPairView):
    """
    Представление для получения токенов авторизации
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Заполнение поля last_login при получении токенов авторизации
        """
        result = super().post(request, *args, **kwargs)
        user = User.objects.get(email=request.data["email"])
        user.last_login = timezone.now()
        user.save()
        return result

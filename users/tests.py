from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


# Create your tests here.
class UserTestCase(APITestCase):
    """
    Тестирование функционала контроллеров User
    """

    def setUp(self):
        """
        Подготовка исходных данных
        """

        self.user = User.objects.create(email="test@email.com")
        self.user.set_password("12345")
        self.user.save()
        self.user_2 = User.objects.create(email="test2@email.com")
        self.user_2.set_password("12345")
        self.user_2.save()
        self.admin = User.objects.create(email="admin@email.com", is_staff=True, is_superuser=True)

        self.client.force_authenticate(self.user)

    def test_user_retrieve(self):
        """
        Тест просмотра объекта User
        """

        # Обычный пользователь - собственный профиль
        url = reverse("users:user", args=[self.user.pk])
        response = self.client.get(url)
        data = response.json()
        data_keys = [key for key in data.keys()]
        result_keys = ['id',
                       'email',
                       'password',
                       'username',
                       'first_name',
                       'last_name',
                       'phone_number',
                       'country',
                       'avatar',
                       'tg_chat_id']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_keys, result_keys)

        # Обычный пользователь - чужой профиль
        url = reverse("users:user", args=[self.admin.pk])
        response = self.client.get(url)
        data = response.json()
        data_keys = [key for key in data.keys()]
        result_keys = ['id',
                       'email',
                       'username',
                       'first_name',
                       'country',
                       'avatar']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_keys, result_keys)

        # Админ
        self.client.force_authenticate(self.admin)
        url = reverse("users:user", args=[self.user.pk])
        response = self.client.get(url)
        data = response.json()
        data_keys = [key for key in data.keys()]
        result_keys = ['id',
                       'email',
                       'password',
                       'username',
                       'first_name',
                       'last_name',
                       'phone_number',
                       'country',
                       'avatar',
                       'tg_chat_id']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_keys, result_keys)

    def test_user_create(self):
        """
        Тест создания объекта User и автоматической активации учетной записи
        """

        url = reverse("users:users")
        data = {
            "email": "test3@email.com",
            "password": "12345"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["is_active"], True)
        self.assertEqual(User.objects.all().count(), 4)

    def test_user_update(self):
        """
        Тест обновления объекта User
        """

        # Обычный пользователь - свой профиль
        url = reverse("users:user", args=[self.user.pk])
        data = {
            "username": "test"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], "test")

        # Обычный пользователь - чужой профиль
        url = reverse("users:user", args=[self.admin.pk])
        data = {
            "username": "test"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Админ - конфиденциальные данные
        self.client.force_authenticate(self.admin)
        url = reverse("users:user", args=[self.user.pk])
        data = {
            "phone_number": "8-800-555-35-35"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["phone_number"], "8-800-555-35-35")

    def test_user_delete(self):
        """
        Тест удаления объекта User
        """

        # Обычный пользователь - свой профиль
        url = reverse("users:user", args=[self.user.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 2)

        # Обычный пользователь - чужой профиль
        url = reverse("users:user", args=[self.admin.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Админ
        self.client.force_authenticate(self.admin)
        url = reverse("users:user", args=[self.user_2.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 1)

    def test_user_list(self):
        """
        Тест вывода списка объектов User
        """

        url = reverse("users:users")
        response = self.client.get(url)
        data = response.json()
        result = [{'id': self.user.pk,
                   'email': self.user.email,
                   'username': self.user.username,
                   'first_name': self.user.first_name,
                   'country': self.user.country,
                   'avatar': None},
                  {'id': self.user_2.pk,
                   'email': self.user_2.email,
                   'username': self.user_2.username,
                   'first_name': self.user_2.first_name,
                   'country': self.user_2.country,
                   'avatar': None},
                  {'id': self.admin.pk,
                   'email': self.admin.email,
                   'username': self.admin.username,
                   'first_name': self.admin.first_name,
                   'country': self.admin.country,
                   'avatar': None}]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_login_refresh(self):
        """
        Тест авторизации и получения access и refresh токенов
        """
        self.client.logout()

        # Проверка авторизации
        url = reverse("users:login")
        data = {
            "email": "test@email.com",
            "password": "12345"
        }
        response = self.client.post(url, data)
        result = response.json()
        result_keys = [key for key in result.keys()]

        self.assertEqual(result_keys, ["refresh", "access"])

        # Проверка обновления access токена по refresh токену
        url = reverse("users:token-refresh")
        data = {
            "refresh": result["refresh"]
        }
        response = self.client.post(url, data)
        result = response.json()

        self.assertTrue(result.get("access"))

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from users.models import User

from .models import Habit, Place


# Create your tests here.
class PlaceTestCase(APITestCase):
    """
    Тестирование функционала контроллеров Place
    """

    def setUp(self):
        """
        Подготовка исходных данных
        """

        self.user = User.objects.create(email="test@email.com")
        self.admin = User.objects.create(email="admin@email.com", is_staff=True, is_superuser=True)

        self.place = Place.objects.create(name="Тестовое место",
                                          owner=self.user)
        self.place_2 = Place.objects.create(name="Тестовое место 2")
        self.client.force_authenticate(self.user)

    def test_place_retrieve(self):
        """
        Тест просмотра объекта Place
        """

        # Обычный пользователь - собственное место
        url = reverse("habits:place", args=[self.place.pk])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.place.name)

        # Обычный пользователь - чужое место
        url = reverse("habits:place", args=[self.place_2.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Админ
        self.client.force_authenticate(self.admin)
        url = reverse("habits:place", args=[self.place.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.place.name)

    def test_place_create(self):
        """
        Тест создания объекта Place и автоматического заполнения поля owner
        """

        # Обычный пользователь
        url = reverse("habits:places")
        data = {
            "name": "Тестовое место 3"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["owner"], self.user.pk)
        self.assertEqual(Place.objects.all().count(), 3)

    def test_place_update(self):
        """
        Тест обновления объекта Place
        """

        # Обычный пользователь - свое место
        url = reverse("habits:place", args=[self.place.pk])
        data = {
            "name": "Проверка обновления данных"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Проверка обновления данных")

        # Обычный пользователь - чужое место
        url = reverse("habits:place", args=[self.place_2.pk])
        data = {
            "name": "Проверка обновления данных"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Админ
        self.client.force_authenticate(self.admin)
        url = reverse("habits:place", args=[self.place.pk])
        data = {
            "name": "Проверка обновления данных"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Проверка обновления данных")

    def test_place_delete(self):
        """
        Тест удаления объекта Place
        """

        # Обычный пользователь - свое место
        url = reverse("habits:place", args=[self.place.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Place.objects.all().count(), 1)

        # Обычный пользователь - чужое место
        url = reverse("habits:place", args=[self.place_2.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Place.objects.all().count(), 1)

        # Админ
        self.client.force_authenticate(self.admin)
        url = reverse("habits:place", args=[self.place_2.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Place.objects.all().count(), 0)

    def test_place_list(self):
        """
        Тест вывода списка объектов Place
        """

        # Обычный пользователь
        url = reverse("habits:places")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = [{'id': self.place.pk,
                   'name': self.place.name,
                   'description': self.place.description,
                   'owner': self.place.owner.pk}]

        self.assertEqual(data, result)

        # Админ
        self.client.force_authenticate(self.admin)
        url = reverse("habits:places")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = [{'id': self.place.pk,
                   'name': self.place.name,
                   'description': self.place.description,
                   'owner': self.place.owner.pk},
                  {'id': self.place_2.pk,
                   'name': self.place_2.name,
                   'description': self.place_2.description,
                   'owner': self.place_2.owner}
                  ]

        self.assertEqual(data, result)


class HabitTestCase(APITestCase):
    """
    Тестирование функционала контроллеров habit
    """

    def setUp(self):
        """
        Подготовка исходных данных
        """

        self.user = User.objects.create(email="test@email.com")
        self.admin = User.objects.create(email="admin@email.com", is_staff=True, is_superuser=True)

        self.place = Place.objects.create(name="Тестовое место", owner=self.user)
        self.habit = Habit.objects.create(time="12:00:00",
                                          action="Тестовая привычка",
                                          frequency=["Пн"],
                                          owner=self.user,
                                          place=self.place)

        self.habit_2 = Habit.objects.create(time="13:00:00",
                                            action="Тестовая привычка 2",
                                            frequency=["Вт"],
                                            owner=self.admin,
                                            place=self.place)

        self.pleasant_habit = Habit.objects.create(time="14:00:00",
                                                   action="Приятная тестовая привычка",
                                                   frequency=["Пн"],
                                                   is_pleasant_habit=True,
                                                   owner=self.user,
                                                   place=self.place)

        self.public_habit = Habit.objects.create(time="15:00:00",
                                                 action="Публичная тестовая привычка",
                                                 frequency=["Пн"],
                                                 is_public=True,
                                                 owner=self.user,
                                                 place=self.place)

        self.client.force_authenticate(self.user)

    def test_habit_retrieve(self):
        """
        Тест просмотра объекта Habit
        """

        # Обычный пользователь - собственная привычка
        url = reverse("habits:habit", args=[self.habit.pk])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

        # Обычный пользователь - чужая привычка
        url = reverse("habits:habit", args=[self.habit_2.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Модератор
        self.client.force_authenticate(self.admin)
        url = reverse("habits:habit", args=[self.habit.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        """
        Тест создания объекта Habit и автоматического заполнения поля owner
        """

        # Обычный пользователь
        url = reverse("habits:habits")
        data = {
            "action": "Тестовая привычка 3",
            "time": "16:00:00",
            "place": self.place.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["owner"], self.user.pk)
        self.assertEqual(Habit.objects.all().count(), 5)

    def test_habit_update(self):
        """
        Тест обновления объекта Habit
        """

        # Обычный пользователь - своя привычка
        url = reverse("habits:habit", args=[self.habit.pk])
        data = {
            "action": "Это моя привычка"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Это моя привычка")

        # Обычный пользователь - чужая привычка
        url = reverse("habits:habit", args=[self.habit_2.pk])
        data = {
            "action": "Это моя привычка"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Админ
        self.client.force_authenticate(self.admin)
        url = reverse("habits:habit", args=[self.habit.pk])
        data = {
            "action": "Это не моя привычка"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Это не моя привычка")

    def test_habit_validators(self):
        """
        Тест валидаторов объекта Habit
        """

        # Одновременный выбор связанной привычки и указание вознаграждения
        url = reverse("habits:habit", args=[self.habit.pk])
        data = {
            "reward": "Тестовое вознаграждения",
            "related_habit": self.pleasant_habit
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesRegex(ValidationError,
                               "Может быть заполнено только одно поле: либо related_habit, либо reward")

        # Время выполнения больше 120 секунд.
        url = reverse("habits:habit", args=[self.habit.pk])
        data = {
            "lead_time": 1200
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesRegex(ValidationError, r"'lead_time': ['Убедитесь, что это значение меньше либо равно 120.']")

        # Выбор связанной привычки, без признака приятной привычки
        url = reverse("habits:habit", args=[self.habit.pk])
        data = {
            "reward": "Тестовое вознаграждения",
            "related_habit": self.habit_2
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesRegex(ValidationError,
                               "Связанная привычка должна быть приятной")

        # Добавление вознаграждения для приятной привычки
        url = reverse("habits:habit", args=[self.pleasant_habit.pk])
        data = {
            "reward": "Тестовое вознаграждение"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesRegex(ValidationError,
                               "У приятной привычки не могут быть заполнены поля: related_habit, reward")

        # # Периодичность меньше одного дня в неделю
        # url = reverse("habits:habit", args=[self.habit.pk])
        # data = {
        #     "frequency": []
        # }
        # response = self.client.patch(url, data)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertRaisesRegex(ValidationError, r"'frequency': ['Этот список не может быть пустым.']")

    def test_habit_delete(self):
        """
        Тест удаления объекта Lesson
        """

        # Обычный пользователь - своя привычка
        url = reverse("habits:habit", args=[self.habit.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 3)

        # Обычный пользователь - чужая привычка
        url = reverse("habits:habit", args=[self.habit_2.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Habit.objects.all().count(), 3)

        # Админ
        self.client.force_authenticate(self.admin)
        url = reverse("habits:habit", args=[self.habit_2.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list(self):
        """
        Тест вывода списка объектов Habit
        """

        # Обычный пользователь
        url = reverse("habits:habits")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {'count': 3,
                  'next': None,
                  'previous': None,
                  'results': [{'id': self.habit.pk,
                               'time': self.habit.time,
                               'action': self.habit.action,
                               'is_pleasant_habit': self.habit.is_pleasant_habit,
                               'frequency': self.habit.frequency,
                               'reward': self.habit.reward,
                               'lead_time': self.habit.lead_time,
                               'is_public': self.habit.is_public,
                               'owner': self.habit.owner.pk,
                               'place': self.habit.place.pk,
                               'related_habit': self.habit.related_habit},
                              {'id': self.pleasant_habit.pk,
                               'time': self.pleasant_habit.time,
                               'action': self.pleasant_habit.action,
                               'is_pleasant_habit': self.pleasant_habit.is_pleasant_habit,
                               'frequency': self.pleasant_habit.frequency,
                               'reward': self.pleasant_habit.reward,
                               'lead_time': self.pleasant_habit.lead_time,
                               'is_public': self.pleasant_habit.is_public,
                               'owner': self.pleasant_habit.owner.pk,
                               'place': self.pleasant_habit.place.pk,
                               'related_habit': self.pleasant_habit.related_habit},
                              {'id': self.public_habit.pk,
                               'time': self.public_habit.time,
                               'action': self.public_habit.action,
                               'is_pleasant_habit': self.public_habit.is_pleasant_habit,
                               'frequency': self.public_habit.frequency,
                               'reward': self.public_habit.reward,
                               'lead_time': self.public_habit.lead_time,
                               'is_public': self.public_habit.is_public,
                               'owner': self.public_habit.owner.pk,
                               'place': self.public_habit.place.pk,
                               'related_habit': self.public_habit.related_habit}]}

        self.assertEqual(data, result)

        # Админ
        self.client.force_authenticate(self.admin)
        url = reverse("habits:habits")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = {'count': 4,
                  'next': None,
                  'previous': None,
                  'results': [{'id': self.habit.pk,
                               'time': self.habit.time,
                               'action': self.habit.action,
                               'is_pleasant_habit': self.habit.is_pleasant_habit,
                               'frequency': self.habit.frequency,
                               'reward': self.habit.reward,
                               'lead_time': self.habit.lead_time,
                               'is_public': self.habit.is_public,
                               'owner': self.habit.owner.pk,
                               'place': self.habit.place.pk,
                               'related_habit': self.habit.related_habit},
                              {'id': self.habit_2.pk,
                               'time': self.habit_2.time,
                               'action': self.habit_2.action,
                               'is_pleasant_habit': self.habit_2.is_pleasant_habit,
                               'frequency': self.habit_2.frequency,
                               'reward': self.habit_2.reward,
                               'lead_time': self.habit_2.lead_time,
                               'is_public': self.habit_2.is_public,
                               'owner': self.habit_2.owner.pk,
                               'place': self.habit_2.place.pk,
                               'related_habit': self.habit_2.related_habit},
                              {'id': self.pleasant_habit.pk,
                               'time': self.pleasant_habit.time,
                               'action': self.pleasant_habit.action,
                               'is_pleasant_habit': self.pleasant_habit.is_pleasant_habit,
                               'frequency': self.pleasant_habit.frequency,
                               'reward': self.pleasant_habit.reward,
                               'lead_time': self.pleasant_habit.lead_time,
                               'is_public': self.pleasant_habit.is_public,
                               'owner': self.pleasant_habit.owner.pk,
                               'place': self.pleasant_habit.place.pk,
                               'related_habit': self.pleasant_habit.related_habit},
                              {'id': self.public_habit.pk,
                               'time': self.public_habit.time,
                               'action': self.public_habit.action,
                               'is_pleasant_habit': self.public_habit.is_pleasant_habit,
                               'frequency': self.public_habit.frequency,
                               'reward': self.public_habit.reward,
                               'lead_time': self.public_habit.lead_time,
                               'is_public': self.public_habit.is_public,
                               'owner': self.public_habit.owner.pk,
                               'place': self.public_habit.place.pk,
                               'related_habit': self.public_habit.related_habit}]}

        self.assertEqual(data, result)

    def test__public_habit_list(self):
        """
        Тест вывода списка публичных объектов Habit
        """

        # Обычный пользователь
        url = reverse("habits:habits-public")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {'count': 1,
                  'next': None,
                  'previous': None,
                  'results': [{'id': self.public_habit.pk,
                               'time': self.public_habit.time,
                               'action': self.public_habit.action,
                               'is_pleasant_habit': self.public_habit.is_pleasant_habit,
                               'frequency': self.public_habit.frequency,
                               'reward': self.public_habit.reward,
                               'lead_time': self.public_habit.lead_time,
                               'is_public': self.public_habit.is_public,
                               'owner': self.public_habit.owner.pk,
                               'place': self.public_habit.place.pk,
                               'related_habit': self.public_habit.related_habit}]}

        self.assertEqual(data, result)

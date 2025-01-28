from django.db import models
from users.models import User


# Create your models here.
class Place(models.Model):
    """
    Модель места для выполнения привычки
    """

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name


class WeekDay(models.Model):
    """
    Модель для недели
    """
    name = models.CharField(max_length=15, verbose_name="Название")

    class Meta:
        verbose_name = "День недели"
        verbose_name_plural = "Дни недели"

    def __str__(self):
        return self.name


class Habit(models.Model):
    """
    Модель привычки
    """
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              verbose_name="Создатель привычки",
                              related_name="habits")
    place = models.ForeignKey(Place,
                              on_delete=models.PROTECT,
                              verbose_name="Место выполнения привычки",
                              related_name="habits")
    time = models.TimeField(verbose_name="Время, когда привычка будет выполняться")
    action = models.CharField(max_length=150, verbose_name="Действие")
    is_pleasant_habit = models.BooleanField(verbose_name="Приятная привычка", default=False)
    related_habit = models.ForeignKey("self",
                                      on_delete=models.SET_NULL,
                                      verbose_name="Связанная привычка",
                                      null=True,
                                      blank=True,
                                      related_name="habits")
    frequency = models.ManyToManyField(WeekDay,
                                       verbose_name="Периодичность",
                                       default=[1, 2, 3, 4, 5, 6, 7])
    reward = models.CharField(max_length=150, verbose_name="Вознаграждение", null=True, blank=True)
    lead_time = models.PositiveSmallIntegerField(default=60, verbose_name="Время на выполнение")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"В {self.frequency} я буду {self.action} в {self.time} в {self.place.name}"

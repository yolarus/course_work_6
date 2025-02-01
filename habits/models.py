from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models
from users.models import User
from src.utils import week_days


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


class Habit(models.Model):
    """
    Модель привычки
    """
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              verbose_name="Создатель привычки",
                              related_name="habits",
                              null=True,
                              blank=True)
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

    frequency = ArrayField(base_field=models.CharField(max_length=2),
                           verbose_name="Периодичность",
                           default=week_days,
                           validators=[MinLengthValidator(1, "Привычка должна выполняться минимум 1 раз в неделю")])
    reward = models.CharField(max_length=150, verbose_name="Вознаграждение", null=True, blank=True)
    lead_time = models.PositiveSmallIntegerField(default=60,
                                                 verbose_name="Время на выполнение",
                                                 validators=[MaxValueValidator(120,
                                                                               "Время выполнения привычки не может "
                                                                               "быть больше 120 секунд")])
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"В {', '.join(self.frequency)} я буду {self.action} в {self.time} в {self.place.name}"

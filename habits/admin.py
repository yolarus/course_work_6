from django.contrib import admin

from .models import Place, WeekDay, Habit


# Register your models here.
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """
    Класс для отображения модели Place в интерфейсе админки
    """
    list_display = ("id", "name")


@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    """
    Класс для отображения модели WeekDay в интерфейсе админки
    """
    list_display = ("id", "name")


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Класс для отображения модели Habit в интерфейсе админки
    """
    list_display = ("id", "action")

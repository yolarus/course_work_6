from rest_framework.exceptions import ValidationError

from .models import Habit


class RelatedHabitOrRewardValidator:
    """
    Проверка, что одновременно не заполнены поле вознаграждения и поле связанной привычки
    """
    def __init__(self, field_1, field_2):
        self.field_1 = field_1
        self.field_2 = field_2

    def __call__(self, value):
        related_habit = value.get(self.field_1)
        reward = value.get(self.field_2)

        if related_habit and reward:
            raise ValidationError("Может быть заполнено только одно поле: либо related_habit, либо reward")


class IsPleasantHabitValidator:
    """
    Проверка, что связанная привычка является приятной
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        related_habit = value.get(self.field)
        if related_habit:
            if not related_habit.is_pleasant_habit:
                raise ValidationError("Связанная привычка должна быть приятной")


class NotRewardOrRelatedHabitValidator:
    """
    Проверка, что у приятной привычки нет вознаграждения или связанной привычки
    """

    def __init__(self, field_1, field_2, field_3):
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def __call__(self, value):
        is_pleasant_habit = value.get(self.field_1)
        related_habit = value.get(self.field_2)
        reward = value.get(self.field_2)

        if is_pleasant_habit and (related_habit or reward):
            raise ValidationError("У приятной привычки не могут быть заполнены поля: related_habit, reward")

from rest_framework import serializers

from .models import Place, Habit
from .validators import RelatedHabitOrRewardValidator, IsPleasantHabitValidator, NotRewardOrRelatedHabitValidator


class PlaceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Place
    """

    class Meta:
        model = Place
        fields = ["id", "name", "description", "owner"]


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit
    """

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [RelatedHabitOrRewardValidator("reward", "related_habit"),
                      IsPleasantHabitValidator("related_habit"),
                      NotRewardOrRelatedHabitValidator("is_pleasant_habit", "related_habit", "reward")]

from rest_framework.exceptions import ValidationError


class RelatedHabitOrRewardValidator:
    """
    Проверка, что одновременно не заполнены поле вознаграждения и поле связанной привычки
    """
    def __init__(self, field_1=None, field_2=None, is_update=None):
        self.field_1 = field_1
        self.field_2 = field_2
        self.is_update = is_update

    def __call__(self, value=None, instance=None, updated_instance=None):

        error = ValidationError("Может быть заполнено только одно поле: либо related_habit, либо reward")

        # Проверка при обновлении
        if self.is_update and updated_instance:
            # Когда related_habit уже было заполнено и при обновлении не удаляется
            if instance.related_habit and updated_instance.related_habit:
                # и в сериализатор передается reward
                if updated_instance.reward:
                    raise error

            # Когда reward уже было заполнено и при обновлении не удаляется
            elif instance.reward and updated_instance.reward:
                # сериализатор передается related_habit
                if updated_instance.related_habit:
                    raise error

        # Проверка при создании и при обновлении, когда поля
        # related_habit и reward одновременно передаются в сериализатор
        elif not self.is_update:
            related_habit = value.get(self.field_1)
            reward = value.get(self.field_2)

            if related_habit and reward:
                raise error


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

    def __init__(self, field_1=None, field_2=None, field_3=None, is_update=None):
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.is_update = is_update

    def __call__(self, value=None, instance=None, updated_instance=None):

        error = ValidationError("У приятной привычки не могут быть заполнены поля: related_habit, reward")

        # Проверка при обновлении
        if self.is_update and updated_instance:
            # Когда is_pleasant_habit уже имело значение True и при обновлении не снимается флаг приятной привычки
            if instance.is_pleasant_habit and updated_instance.is_pleasant_habit:
                # и в сериализатор передаются поля related_habit / reward
                if updated_instance.related_habit or updated_instance.reward:
                    raise error
            # Когда поля related_habit / reward уже имели значения и не были удалены при обновлении
            elif ((instance.related_habit or instance.reward)
                  and (updated_instance.related_habit or updated_instance.reward)):
                # и устанавливается флаг приятной привычки
                if updated_instance.is_pleasant_habit:
                    raise error

        # Проверка при создании и при обновлении, когда поля
        # related_habit / is_pleasant_habit и reward одновременно передаются в сериализатор
        elif not self.is_update:
            is_pleasant_habit = value.get(self.field_1)
            related_habit = value.get(self.field_2)
            reward = value.get(self.field_3)
            if is_pleasant_habit and (related_habit or reward):
                raise error

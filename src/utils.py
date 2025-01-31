def get_queryset_for_owner(user, queryset):
    """
    Выборка списка объектов только для их владельцев
    """
    if user.is_superuser:
        return queryset.order_by("id")
    return queryset.filter(owner=user).order_by("id")


def week_days():
    """
    Возвращает список дней недели
    """
    return ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

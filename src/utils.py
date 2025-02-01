import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_URl


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


def send_telegram_message(chat_id, message):
    """
    Отправка сообщения в ТГ
    """
    params = {
        'text': message,
        'chat_id': chat_id}
    requests.get(f'{TELEGRAM_URl}{TELEGRAM_BOT_TOKEN}/sendMessage', params=params)

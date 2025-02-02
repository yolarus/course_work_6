import datetime

from celery import shared_task

from src.utils import send_telegram_message, week_days

from .models import Habit


@shared_task()
def habits_scheduler():
    """
    Рассылка уведомлений пользователям с напоминанием о привычке
    """
    today = datetime.datetime.now()
    weekday = week_days()[today.weekday()]
    current_time = today.time()
    habits = Habit.objects.all()

    for habit in habits:
        if weekday in habit.frequency:
            if habit.time.hour == current_time.hour and habit.time.minute == current_time.minute:
                print("Yoj")
                send_telegram_message(habit.owner.tg_chat_id, str(habit))

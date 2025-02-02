from django.core.management import call_command
from django.core.management.base import BaseCommand

from habits.models import Place, Habit


class Command(BaseCommand):
    """
    Заполнение БД фикстурой сообщений, получателей, рассылок и их попыток сервиса рассылок
    """

    def handle(self, *args: list, **kwargs: dict) -> None:

        Place.objects.all().delete()
        Habit.objects.all().delete()

        call_command('loaddata', 'habits.json')

        self.stdout.write(self.style.SUCCESS("Фикстуры из файла habits.json успешно загружены"))

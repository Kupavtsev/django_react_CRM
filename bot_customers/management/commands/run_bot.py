# from django.core.management import BaseCommand
from django.core.management.base import BaseCommand
# from bot_customers.bot import bot


class Command(BaseCommand):
    def handle(self, *args, **options):
        from bot_customers.bot import bot
        bot.run()


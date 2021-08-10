from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from bot_customers.bot import bot
        bot.run()


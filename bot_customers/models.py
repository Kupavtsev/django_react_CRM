from django.db import models


class UserTelegram(models.Model):

    first_name  = models.CharField("First name", max_length=255)
    last_name   = models.CharField("Last name", max_length=255)
    email   	= models.EmailField(verbose_name="email", max_length=60, unique=True)
    telegram_id = models.IntegerField(null=False, unique=True)
    phone       = models.CharField(max_length=25)
    city        = models.TextField(blank=True, null=True)
    link        = models.TextField(blank=True, null=True)

    def __int__(self):
        return self.telegram_id
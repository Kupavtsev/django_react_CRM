from django.db import models


class UserTelegram(models.Model):

    first_name  = models.CharField(verbose_name="First name", null=True, max_length=255)
    last_name   = models.CharField(verbose_name="Last name", null=True, max_length=255)
    email   	= models.EmailField(verbose_name="E-mail", max_length=60, unique=True)
    telegram_id = models.IntegerField(verbose_name='Telega id', null=False, unique=True)
    phone       = models.CharField(max_length=25, null=True)
    city        = models.TextField(blank=True, null=True)
    link        = models.TextField(blank=True, null=True)
    registred   = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Зарегестрирован")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Аккаунты от Телеги'
        verbose_name        = 'Аккаунт Телеги'
        ordering            = ['-registred']

class UserTelegramRegister:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name  = None
        self.email      = None
        self.telegram_id= None
        self.phone      = None

        def __str__(self):
            return self.first_name

class Customers:
    def __init__(self, first_name):
        self.first_name     = first_name
        self.last_name      = None
        self.email          = None
        self.phone          = None
        self.address        = None
        self.description    = None
        # self.createdAt = None

        def __str__(self):
            return self.first_name
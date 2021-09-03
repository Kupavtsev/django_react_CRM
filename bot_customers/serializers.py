from rest_framework     import serializers
from customers.models   import Customer
from .models            import UserTelegram


class CustomerSerializer( serializers.ModelSerializer ):

    class Meta:
        model   = Customer
        fields  = ('pk',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'address',
                  'description',
                  'telegram_id')

class TelegramUserSerialazer( serializers.ModelSerializer ):
    class Meta:
        model   = UserTelegram
        fields  = ('pk',
                  'first_name',
                  'last_name',
                  'email',
                  'telegram_id',
                  'phone',
                  'city',
                  'link'
        )
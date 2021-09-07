# -*- coding: utf-8 -*-
# Telegram
# from customers.models import Customer
import telebot
from telebot                    import types
from rest_framework.response    import Response
from rest_framework             import status

from .models                    import UserTelegram, Customers, UserTelegramRegister
from .serializers               import *
from .config                    import TOKEN


# =======================================
# This is just info!!!
tele_users = UserTelegram.objects.all()
# exact_tele_user = tele_users[1].telegram_id

# users = tele_users[:].telegram_id
tele_users_list = []
for user in tele_users:
    tele_users_list.append(user.telegram_id)
    print('user.telegram_id: ', user.telegram_id)
print('tele_users_list: ', tele_users_list)
# =========================================



bot                         = telebot.TeleBot(TOKEN)

telegram_user_dict : dict   = {}
customers_dict : dict       = {}


 # Handle '/start' and '/help'
@bot.message_handler( commands=['help', 'start'] )
# Add menu with buttons
def send_welcome(message):
    user_id     = message.from_user.id
    chat_id     = message.chat.id
    username    = message.from_user.full_name
    try:
        UserTelegram.objects.get( telegram_id = user_id )
        msg = bot.send_message( chat_id, f'Здравствуйте {username}👋\nYour id is {user_id}\nВведите имя клиента: ' )
        bot.register_next_step_handler( msg, process_last_name_step )
    except: 
        msg = bot.send_message( chat_id, f'Здравствуйте {username}👋\nYour id {user_id} is not registred\n\nВам необходимо зарегестрироваться!\nВведите ваше имя: ' )
        bot.register_next_step_handler( msg, process_registration_step )

def process_last_name_step( message ):
    try:
        chat_id                 = message.chat.id
        first_name              = message.text
        user                    = Customers( first_name )
        customers_dict[chat_id] = user
        msg                     = bot.send_message( chat_id, 'Введите фамилию клиента:' )
        # msg = bot.reply_to(message, 'Введите фамилию клиента:')
        bot.register_next_step_handler( msg, process_email_step )
    except Exception as e:
        bot.reply_to( message, 'process_last_name_step' ) 

def process_email_step( message ):
    # Add email RE check
    try:
        chat_id         = message.chat.id
        last_name       = message.text
        user            = customers_dict[chat_id]
        user.last_name  = last_name
        msg             = bot.send_message( chat_id, 'Введите email клиента:' )
        # msg = bot.reply_to(message, 'Введите email клиента:')
        bot.register_next_step_handler( msg, process_phone_step )
    except Exception as e:
        bot.reply_to( message, 'process_email_step' ) 

def process_phone_step( message ):
    # Add RE phone check
    try:
        chat_id     = message.chat.id
        email       = message.text
        user        = customers_dict[chat_id]
        user.email  = email
        msg         = bot.send_message( chat_id, 'Введите телефон клиента:' )
        # msg = bot.reply_to(message, 'Введите телефон клиента:')
        bot.register_next_step_handler( msg, process_address_step )
    except Exception as e:
        bot.reply_to( message, 'process_phone_step' ) 
# ===============
def process_address_step( message ):
    try:
        chat_id     = message.chat.id
        phone       = message.text
        user        = customers_dict[chat_id]
        user.phone  = phone
        msg         = bot.send_message( chat_id, 'Введите адрес клиента:' )
        # msg = bot.reply_to(message, 'Введите адрес клиента:')
        bot.register_next_step_handler( msg, process_description_step )
    except Exception as e:
        bot.reply_to( message, 'process_address_step' )

def process_description_step( message ):
    try:
        chat_id     = message.chat.id
        address     = message.text
        user        = customers_dict[chat_id]
        user.address= address
        msg         = bot.send_message( chat_id, 'Введите описание клиента:' )
        # msg = bot.reply_to(message, 'Введите описание клиента:')
        bot.register_next_step_handler (msg, process_post_data_step )
    except Exception as e:
        bot.reply_to( message, 'process_description_step' ) 

def process_post_data_step(message):
# Two variants via POST request or direct to Base
    try:
        telegram_id         = int(message.from_user.id)
        chat_id             = message.chat.id
        user                = customers_dict[chat_id]
        description         = message.text
        user.description    = description
        print( 'first_name: ',   user.first_name )
        print( 'last_name: ',    user.last_name )
        print( 'email: ',        user.email )
        print( 'phone: ',        user.phone )
        print( 'address: ',      user.address )
        print( 'description: ',  user.description )
        print( 'telegram_id: ',  telegram_id )
        print( '--------------------' )
        data = {
            "first_name"    : user.first_name,
            "last_name"     : user.last_name,
            "email"         : user.email,
            "phone"         : user.phone,
            "address"       : user.address,
            "description"   : user.description,
            "telegram_id"   : telegram_id
        }
        print('Fullfield data: ', data)

        # Keyboard restart
        markup_restart = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard = True)
        button_restart = types.KeyboardButton(text='начать заново')
        markup_restart.add(button_restart)
        msg = bot.send_message(chat_id, 'Вы добавили нового клиента\n\nСпасибо за то, что воспользовались нашим сервисом 🙏', reply_markup=markup_restart)

        form = msg.text
        if (form == u'Вы добавили нового клиента\n\nСпасибо за то, что воспользовались нашим сервисом 🙏'):
            bot.register_next_step_handler(msg, send_welcome)
        else: print('else')
        # # Keyboard restart end

        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        bot.reply_to(message, 'process_post_data_step')



# ===========================================================================
#                      Registration
# ===========================================================================


def process_registration_step( message ):
    try:
        chat_id                     = message.chat.id
        first_name                  = message.text
        user                        = UserTelegramRegister( first_name )
        telegram_user_dict[chat_id] = user
        msg = bot.send_message( chat_id, 'Введите фамилию нового пользователя.' )
        # msg = bot.reply_to(message, 'Введите фамилию клиента:')
        bot.register_next_step_handler( msg, process_registration_email_step )
    except Exception as e:
        bot.reply_to( message, 'process_registration_step' ) 

def process_registration_email_step( message ):
    try:
        chat_id         = message.chat.id
        last_name       = message.text
        user            = telegram_user_dict[chat_id]
        user.last_name  = last_name
        msg             = bot.send_message( chat_id, 'Введите email нового пользователя.' )
        # msg = bot.reply_to(message, 'Введите email клиента:')
        bot.register_next_step_handler( msg, process_registration_post_step )
    except Exception as e:
        bot.reply_to( message, 'process_registration_post_step' )

def process_registration_post_step( message ):
    try:
        telegram_id         = int(message.from_user.id)
        chat_id             = message.chat.id
        email               = message.text
        user                = telegram_user_dict[chat_id]
        user.email          = email
        data = {
            "first_name"    : user.first_name,
            "last_name"     : user.last_name,
            "email"         : user.email,
            "telegram_id"   : telegram_id,
            "phone"         : '143',
        }
        print( 'Fullfield data: ', data )

         # Keyboard restart
        markup_restart = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard = True)
        button_restart = types.KeyboardButton(text='начать заново')
        markup_restart.add(button_restart)
        msg = bot.send_message(chat_id, 'Вы добавили нового пользователя Телеги\n\nСпасибо за то, что воспользовались нашим сервисом 🙏', reply_markup=markup_restart)

        form = msg.text
        if (form == u'Вы добавили нового пользователя Телеги\n\nСпасибо за то, что воспользовались нашим сервисом 🙏'):
            bot.register_next_step_handler(msg, send_welcome)
        else: print('else')
        # # Keyboard restart end

        serializer = TelegramUserSerialazer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except:
         bot.reply_to(message, 'process_registration_post_step')

         
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.polling()
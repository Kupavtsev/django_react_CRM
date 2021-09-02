# -*- coding: utf-8 -*-
# Telegram
# from customers.models import Customer
import telebot
from telebot import types
from rest_framework.response import Response
from rest_framework import status

from .models import UserTelegram
from .serializers import *
from .config import TOKEN

# Я могу создать массив из айдишников или обращаться к конкретному айди

tele_users = UserTelegram.objects.all()
print(type(tele_users))
print(len(tele_users))
exact_tele_user = tele_users[1].telegram_id
# users = tele_users[:].telegram_id
# tele_users_list = []
# for user in tele_users:
#     tele_users_list.append(user.telegram_id)
#     print('user.telegram_id: ', user.telegram_id)
# print('exact_tele_user: ', users)
# print(type(users))

bot = telebot.TeleBot(TOKEN)

customers_dict : dict = {}

class Customers:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = None
        self.email = None
        self.phone = None
        self.address = None
        self.description = None
        # self.createdAt = None

        def __str__(self):
            return self.first_name


    # Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
# Add check if user registred
# Add menu with buttons
def send_welcome(message):
    chat_id = message.chat.id
    username = message.from_user.full_name
    user_id = message.from_user.id
    msg = bot.send_message(chat_id, f'Здравствуйте {username}👋\nYour id is {user_id}\nВведите имя клиента: ')
    bot.register_next_step_handler(msg, process_last_name_step)

def process_last_name_step(message):
    try:
        chat_id = message.chat.id
        first_name = message.text
        user = Customers(first_name)
        customers_dict[chat_id] = user
        msg = bot.send_message(chat_id, 'Введите фамилию клиента:')
        # msg = bot.reply_to(message, 'Введите фамилию клиента:')
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        bot.reply_to(message, 'process_last_name_step') 

def process_email_step(message):
    # Add email RE check
    try:
        chat_id = message.chat.id
        last_name = message.text
        user = customers_dict[chat_id]
        user.last_name = last_name
        msg = bot.send_message(chat_id, 'Введите email клиента:')
        # msg = bot.reply_to(message, 'Введите email клиента:')
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        bot.reply_to(message, 'process_email_step') 

def process_phone_step(message):
    # Add RE phone check
    try:
        chat_id = message.chat.id
        email = message.text
        user = customers_dict[chat_id]
        user.email = email
        msg = bot.send_message(chat_id, 'Введите телефон клиента:')
        # msg = bot.reply_to(message, 'Введите телефон клиента:')
        bot.register_next_step_handler(msg, process_address_step)
    except Exception as e:
        bot.reply_to(message, 'process_phone_step') 
# ===============
def process_address_step(message):
    try:
        chat_id = message.chat.id
        phone = message.text
        user = customers_dict[chat_id]
        user.phone = phone
        msg = bot.send_message(chat_id, 'Введите адрес клиента:')
        # msg = bot.reply_to(message, 'Введите адрес клиента:')
        bot.register_next_step_handler(msg, process_description_step)
    except Exception as e:
        bot.reply_to(message, 'process_address_step')

def process_description_step(message):
    try:
        chat_id = message.chat.id
        address = message.text
        user = customers_dict[chat_id]
        user.address = address
        msg = bot.send_message(chat_id, 'Введите описание клиента:')
        # msg = bot.reply_to(message, 'Введите описание клиента:')
        bot.register_next_step_handler(msg, process_post_data_step)
    except Exception as e:
        bot.reply_to(message, 'process_description_step') 

def process_post_data_step(message):
# Two variants via POST request or direct to Base
    try:
        telegram_id = int(message.from_user.id)
        chat_id = message.chat.id
        user = customers_dict[chat_id]
        description = message.text
        user.description = description
        print('first_name: ', user.first_name)
        print('last_name: ', user.last_name)
        print('email: ', user.email)
        print('phone: ', user.phone)
        print('address: ', user.address)
        print('description: ', user.description)
        print('telegram_id: ', telegram_id)
        print('--------------------')
        data = {
            "first_name" :  user.first_name,
            "last_name" :  user.last_name,
            "email" :  user.email,
            "phone" :  user.phone,
            "address" :  user.address,
            "description" :  user.description,
            "telegram_id" : telegram_id
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

    



bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()
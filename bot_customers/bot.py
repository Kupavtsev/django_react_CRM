# -*- coding: utf-8 -*-
# Telegram
from customers.models import Customer
import telebot
from telebot import types

from config import TOKEN, EMAIL_PASSWORD

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
        self.createdAt = None

        def __str__(self):
            return self.first_name


    # Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Введите имя клиента: ')
    bot.register_next_step_handler(msg, process_last_name_step)

def process_last_name_step(message):
    try:
        chat_id = message.chat.id
        first_name = message.text
        user = Customers(first_name)
        customers_dict[chat_id] = user
        msg = bot.reply_to(message, 'Введите фамилию клиента:')
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        bot.reply_to(message, 'process_last_name_step') 

def process_email_step(message):
    try:
        chat_id = message.chat.id
        last_name = message.text
        user = customers_dict[chat_id]
        user.last_name = last_name
        msg = bot.reply_to(message, 'Введите email клиента:')
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        bot.reply_to(message, 'process_email_step') 

def process_phone_step(message):
    try:
        chat_id = message.chat.id
        email = message.text
        user = customers_dict[chat_id]
        user.email = email
        msg = bot.reply_to(message, 'Введите телефон клиента:')
        bot.register_next_step_handler(msg, process_address_step)
    except Exception as e:
        bot.reply_to(message, 'process_phone_step') 
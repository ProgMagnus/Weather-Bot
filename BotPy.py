from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps
import telebot
import random
from telebot import types

config_dict = get_default_config()
config_dict['language'] = 'RU'
owm = OWM('Your token', config_dict)
mgr = owm.weather_manager()

bot = telebot.TeleBot("Your token") 

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nя - <b>{1.first_name}</b>, метео-бот, просто напиши свой город и я подскажу погоду".format(message.from_user, bot.get_me()),
                     parse_mode ='html' )

@bot.message_handler(content_types=['text'])
def send_echo(message):
    observation = mgr.weather_at_place(message.text)
    w = observation.weather
    temp = w.temperature('celsius')['temp']

    answer = "В городе " + message.text + " сейчас " + w.detailed_status + "\n"
    answer += "Температура около " + str(temp) + "\n\n"
    if temp > 20:
        answer += "На улице тепло. Самое время для шорт."
    elif temp > 15:
        answer += "Достаточно надеть футболку."
    elif temp > 10:
        answer += "Возьмите с собой кофту."
    elif temp > 5:
        answer += "Прохладно. Наденьте куртку."
    elif temp > 0:
        answer += "Шапка не помешает."
    elif temp < 0:
        answer += "Холодно. Одевайтесь потеплее."
    elif temp < -5:
        answer += "Нужна теплая одежда. Больше теплой одежды."
    elif temp < -10:
        answer += "Воробьи замерзли на деревьях. Шуба не помешает."
    else:
        answer += "Морозный ад. Лучше оставайтесь дома."
    bot.send_message(message.chat.id, answer)

bot.polling( none_stop = True)

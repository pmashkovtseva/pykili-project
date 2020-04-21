import telebot
from telebot import apihelper
from telebot import types
import random

apihelper.proxy = {}

bot = telebot.TeleBot()

@bot.message_handler(commands = ['start'])
def hello(message):
    bot.send_message(message.from_user.id, 'Привет! Я Кинобот. Умею рекомендовать фильмы из Топ-500 Кинопоиска по твоим запросам.')
    bot.send_message(message.from_user.id, 'Пожалуйста, ознакомься с разделом /help перед началом работы. Чтобы приступить к выбору фильма, введи /movie.')

@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.from_user.id, 'Начать поиск фильма можно командой /movie.')
    bot.send_message(message.from_user.id, 'Доступные для поска жанры:')
    bot.send_message(message.from_user.id, 'Аниме\nБиография\nБоевик\nВестерн\nВоенный\nДетектив\nДрама\nИстория\nКомедия\nКриминал\nМелодрама\nМузыка\nМультфильм\nМюзикл\nПриключения\nСемейный\nСпорт\nТриллер\nУжасы\nФантастика\nФильм-нуар\nФэнтези')

@bot.message_handler(commands = ['movie'])
def start(message):
    bot.send_message(message.from_user.id, 'Выбери жанр фильма.')
    bot.register_next_step_handler(message, get_genre)

def get_genre(message):
    global genre
    genre = message.text.lower()
    bot.send_message(message.from_user.id, 'Ввведи желаемую страну производства.')
    bot.register_next_step_handler(message, get_country)

def get_country(message):
    global country
    country = message.text
    bot.send_message(message.from_user.id, 'Введи год, раньше которого фильмы не будут выбираться.')
    bot.register_next_step_handler(message, get_minyear)

def get_minyear(message):
    global minyear
    minyear = message.text
    bot.send_message(message.from_user.id, 'Введи год, позже которого фильмы не будут выбираться.')
    bot.register_next_step_handler(message, get_maxyear)

def get_maxyear(message):
    global maxyear
    maxyear = message.text
    bot.send_message(message.from_user.id, 'Ищем фильм по следующим параметрам. Для продолжения введи "ОК".')
    bot.register_next_step_handler(message, finish)

def finish(message):
    bot.send_message(message.from_user.id, '\nЖанр: ' + genre + '\n' + 'Страна: ' + country + '\n' + 'Минимальный год выпуска: ' + str(minyear) + '\n' + 'Максимальный год выпуска: ' + str(maxyear))
    with open('top.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            for year in range(int(minyear), int(maxyear)):
                if str(year) in line:
                    if genre in line:
                        if country in line:
                            with open('results.txt', 'w', encoding = 'utf-8') as f1:
                                f1.write(line)
                            with open('results.txt', encoding = 'utf-8') as f2:
                                text = f2.readlines()
                            result = random.sample(text, 1)
    bot.send_message(message.from_user.id, result)
    bot.send_message(message.from_user.id, 'Попробуем снова?')

bot.polling()

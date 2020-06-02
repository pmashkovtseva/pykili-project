import telebot
from telebot import apihelper
from telebot import types
import random


apihelper.proxy = {''}

bot = telebot.TeleBot('')

@bot.message_handler(commands = ['start'])
def hello(message):
    bot.send_message(message.from_user.id, 'Привет! Я Кинобот. Умею рекомендовать фильмы из Топ-500 Кинопоиска по твоим запросам.')
    bot.send_message(message.from_user.id, 'Пожалуйста, ознакомься с разделом /help перед началом работы. Чтобы приступить к выбору фильма, введи /movie.')

@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.from_user.id, 'Начать поиск фильма можно командой /movie. Пропустить одну или несколько опций поиска можно, введя \'пропустить\'.\n\nКомандой /random можно выбрать случайный фильм из всего топа.')
    bot.send_message(message.from_user.id, 'Доступные для поска жанры:')
    bot.send_message(message.from_user.id, 'Аниме\nБиография\nБоевик\nВестерн\nВоенный\nДетектив\nДрама\nИстория\nКомедия\nКриминал\nМелодрама\nМузыка\nМультфильм\nМюзикл\nПриключения\nСемейный\nСпорт\nТриллер\nУжасы\nФантастика\nФильм-нуар\nФэнтези')
    bot.send_message(message.from_user.id, 'Доступных для поиска стран очень много, так что feel free to explore :)')

@bot.message_handler(commands = ['random'])
def random_result(message):
    with open('top.txt', 'r', encoding = 'utf-8') as f:
        lines = f.read().splitlines()
        line = random.sample(lines, 1)
    bot.send_message(message.from_user.id, line)
    bot.send_message(message.from_user.id, 'Попробуем еще?')

@bot.message_handler(commands = ['movie'])
def start(message):
    bot.send_message(message.from_user.id, 'Выбери жанр фильма.')
    bot.register_next_step_handler(message, get_genre)

def get_genre(message):
    global genre
    genre = message.text.lower()
    nextstep = 'пропустить'
    if genre == nextstep.lower():
        genre = ''
    bot.send_message(message.from_user.id, 'Ввведи желаемую страну производства.')
    bot.register_next_step_handler(message, get_country)

def get_country(message):
    global country
    country = message.text.capitalize()
    nextstep = 'пропустить'
    if country == nextstep.lower():
        country = ''
    bot.send_message(message.from_user.id, 'Введи год, раньше которого фильмы не будут выбираться.')
    bot.register_next_step_handler(message, get_minyear)

def get_minyear(message):
    global minyear
    minyear = message.text
    nextstep = 'пропустить'
    if minyear == nextstep.lower():
        minyear = ''
    bot.send_message(message.from_user.id, 'Введи год, позже которого фильмы не будут выбираться.')
    bot.register_next_step_handler(message, get_maxyear)

def get_maxyear(message):
    global maxyear
    maxyear = message.text
    nextstep = 'пропустить'
    if maxyear == nextstep.lower():
        maxyear = ''
    bot.send_message(message.from_user.id, 'Ищем фильм по заданным параметрам. Для продолжения введи "ОК".')
    bot.register_next_step_handler(message, finish)

def finish(message):
    bot.send_message(message.from_user.id, '\nЖанр: ' + genre + '\n' + 'Страна: ' + country + '\n' + 'Минимальный год выпуска: ' + str(minyear) + '\n' + 'Максимальный год выпуска: ' + str(maxyear))
    result = ''
    with open('top.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if genre != '' and country != '' and minyear != '' and maxyear != '':
                for year in range(int(minyear), int(maxyear)):
                    if str(year) in line and genre in line and country in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre == '' and country != '' and minyear != '' and maxyear != '':
                for year in range(int(minyear), int(maxyear)):
                    if str(year) in line and country in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre != '' and country == '' and minyear != '' and maxyear != '':
                for year in range(int(minyear), int(maxyear)):
                    if str(year) in line and genre in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre != '' and country != '' and minyear == '' and maxyear != '':
                for year in range (0, int(maxyear)):
                    if str(year) in line and genre in line and country in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre != '' and country != '' and minyear != '' and maxyear == '':
                for year in range (int(minyear), 2020):
                    if str(year) in line and genre in line and country in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre == '' and country == '' and minyear != '' and maxyear != '':
                for year in range(int(minyear), int(maxyear)):
                    if str(year) in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre == '' and country != '' and minyear == '' and maxyear != '':
                for year in range(0, int(maxyear)):
                    if str(year) in line and country in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre == '' and country != '' and minyear != '' and maxyear == '':
                for year in range(int(minyear), 2021):
                    if str(year) in line and country in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre != '' and country == '' and minyear != '' and maxyear == '':
                for year in range(int(minyear), 2021):
                    if str(year) in line and genre in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre != '' and country == '' and minyear == '' and maxyear != '':
                for year in range(0, int(maxyear)):
                    if str(year) in line and country in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1) 
            if genre != '' and country != '' and minyear == '' and maxyear == '':
                for year in range(0, 2021):
                    if str(year) in line and genre in line and country in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre != '' and country == '' and minyear == '' and maxyear == '':
                for year in range(0, 2021):
                    if str(year) in line and genre in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre == '' and country != '' and minyear == '' and maxyear == '':
                for year in range(0, 2021):
                    if str(year) in line and country in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre == '' and country == '' and minyear != '' and maxyear == '':
                for year in range(int(minyear), 2021):
                    if str(year) in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre == '' and country == '' and minyear == '' and maxyear != '':
                for year in range(0, int(maxyear)):
                    if str(year) in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)
            if genre == '' and country == '' and minyear == '' and maxyear == '':
                for year in range(0, 2021):
                    if str(year) in line:
                        with open('results.txt', 'w', encoding = 'utf-8') as f1:
                            f1.write(line)
                        with open('results.txt', encoding = 'utf-8') as f2:
                            text = f2.readlines()
                        result = random.sample(text, 1)         
    if result != '':
        bot.send_message(message.from_user.id, result)
    else:
        bot.send_message(message.from_user.id, 'О нет! Кажется, по заданным параметрам ничего не найдено.')
    bot.send_message(message.from_user.id, 'Попробуем снова?')

bot.polling()

# -*- coding: utf-8 -*-

# import random
import telebot

import pdfcrowd
from pdfkit import from_file
import pdfkit

import time
import datetime
import re
import numpy as np
from emoji import emojize
from telebot import types
from data.banned import Ban
from data.people import People
from data.boss import Boss
from data.nejronka import Data
from data import db_session

SMILE = ['↩', "🏠", "🤍", "❤"]
SINONIMS = {'python': {'питон', "пайтон", 'pyton', "piton", "puthon", "python"},
            'frontend': {'фронтэнд', "фронт-энд", "фронтенд", "фронт-енд", "front", "front-end", "frontend"},
            'backend': {'бэкэнд', 'бэкенд', "бэк-энд", "бекенд", "бекенд-енд", "back", "back-end", "backend"},
            'java': {'ява', "жава", "джава", 'java'},
            "javascript": {'javascript', "js", "java-script"},
            "web": {"web", 'веб', "вэб"},
            '1c': {'1c', '1с'}
            }
jobs = {"программист", "разработчик", 'java', '4th dimension/4d', 'abap', 'abc', 'actionscript', 'ada', 'agilent vee',
        'algol',
        'alice',
        'angelscript', 'apex', 'apl', 'applescript', 'arc', 'arduino', 'asp', 'aspectj', 'assembly',
        'atlas', 'augeas', 'autohotkey', 'autoit', 'autolisp', 'automator', 'avenue', 'awk', 'bash',
        '(visual) basic', 'bc', 'bcpl', 'beta', 'blitzmax', 'boo', 'bourne shell', 'bro', 'c', 'c shell',
        'c#', 'c++', 'c++/cli', 'c-omega', 'caml', 'ceylon', 'cfml', 'cg', 'ch', 'chill', 'cil',
        'cl (os/400)', 'clarion', 'clean', 'clipper', 'clojure', 'clu', 'cobol', 'cobra', 'coffeescript',
        'coldfusion', 'comal', 'common lisp', 'coq', 'ct', 'curl', 'd', 'dart', 'dcl', 'dcpu-16 asm',
        'delphi/object pascal', 'dibol', 'dylan', 'e', 'ec', 'ecl', 'ecmascript', 'egl', 'eiffel', 'elixir',
        'emacs lisp', 'erlang', 'etoys', 'euphoria', 'exec', 'f#', 'factor', 'falcon', 'fancy', 'fantom',
        'felix', 'forth', 'fortran', 'fortress', '(visual) foxpro', 'gambas', 'gnu octave', 'go',
        'google appsscript', 'gosu', 'groovy', 'haskell', 'haxe', 'heron', 'hpl', 'hypertalk', 'icon',
        'idl', 'inform', 'informix-4gl', 'intercal', 'io', 'ioke', 'j', 'j#', 'jade', 'java',
        'java fx script', 'javascript', 'jscript', 'jscript.net', 'julia', 'korn shell', 'kotlin',
        'labview', 'ladder logic', 'lasso', 'limbo', 'lingo', 'lisp', 'logo', 'logtalk', 'lotusscript',
        'lpc', 'lua', 'lustre', 'm4', 'mad', 'magic', 'magik', 'malbolge', 'mantis', 'maple', 'mathematica',
        'matlab', 'max/msp', 'maxscript', 'mel', 'mercury', 'mirah', 'miva', 'ml', 'monkey', 'modula-2',
        'modula-3', 'moo', 'moto', 'ms-dos batch', 'mumps', 'natural', 'nemerle', 'nimrod', 'nqc', 'nsis',
        'nu', 'nxt-g', 'oberon', 'object rexx', 'objective-c', 'objective-j', 'ocaml', 'occam', 'ooc',
        'opa', 'opencl', 'openedge abl', 'opl', 'oz', 'paradox', 'parrot', 'pascal', 'perl', 'php', 'pike',
        'pilot', 'pl/i', 'pl/sql', 'pliant', 'postscript', 'pov-ray', 'powerbasic', 'powerscript',
        'powershell', 'processing', 'prolog', 'puppet', 'pure data', 'python', 'q', 'r', 'racket',
        'realbasic', 'rebol', 'revolution', 'rexx', 'rpg (os/400)', 'ruby', 'rust', 's', 's-plus', 'sas',
        'sather', 'scala', 'scheme', 'scilab', 'scratch', 'sed', 'seed7', 'self', 'shell', 'signal',
        'simula', 'simulink', 'slate', 'smalltalk', 'smarty', 'spark', 'spss', 'sqr', 'squeak', 'squirrel',
        'standard ml', 'suneido', 'supercollider', 'tacl', 'tcl', 'tex', 'thinbasic', 'tom', 'transact-sql',
        'turing', 'typescript', 'vala/genie', 'vbscript', 'verilog', 'vhdl', 'viml', 'visual basic .net',
        'webdna', 'whitespace', 'x10', 'xbase', 'xbase++', 'xen', 'xpl', 'xslt', 'xquery', 'yacc', 'yorick',
        'z shell', 'css', 'html', 'js', 'верстка', 'crm', 'gulp', 'sass', 'vue', '1c', '1с', 'sql', 'ооп',
        'web', 'wordpress', 'seo', 'git', 'react', 'тестировщик', 'backend', 'специалист баз данных', 'mvc',
        'фронтэнд', 'developer', 'frontend', 'junior', 'middle', 'senior', 'django', 'flask', 'swift',
        'desktop', 'diy', 'pet', 'геймдев', 'gamedev', '.net', 'front-end', 'wpf', 'excel', 'cisco', 'aws',
        'server', 'xml', 'android', 'json', 'андроит', 'jquery', 'bootstrap', 'bitrix', 'laravel',
        'symfony', 'codeigniter', 'yii', 'phalcon', 'cakephp', 'zend', 'slim', 'fuelphp', 'phpixie',
        'joomla', 'bitrix', 'drupal', 'wordpress', 'opencart', 'питон', 'программист'}
# bot = telebot.TeleBot(open('data/media/token.txt').read())
bot = telebot.TeleBot('1630042590:AAHL1L9W0v23YoHuuDU7Z2a4rbDBg76xoZA')
print('\033[35mStarting.....')
count = -1
history = True
print('\033[35mConnecting to db....')
try:
    db_session.global_init("db/resume.sqlite")
except Exception:
    db_session.global_init("/home/AVI2005/TelegrammBot/db/resume.sqlite")
print('\033[35mDb was conected...')


def tconv(x):
    """
    :param x: int; хз что передаётся, вроде секунды
    :return: str; нормально выглядещую дату и время
    """
    return time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))


def correctemail(email):
    if email.count('@') > 1 or email.count('@') == 0:
        return False
    [name, domain] = email.split('@')
    if len(domain) > 256:
        return False
    if domain.count('.') == 0:
        return False
    includedomain = domain.split('.')
    # список с кодами корректных сиволов a-z - и _
    correctchrlist = list(range(ord('a'), ord('z') + 1))
    correctchrlist.extend([ord('-'), ord('_')])
    for k in includedomain:
        # проверяем нет ли пустых подстрок в домене
        if k == '':
            return False
        # проверяем нет ли нелегальных символов в подстроках в домене
        for n in k:
            if ord(n) not in correctchrlist:
                errormsg = "Недопустимый символ " + n
                return (False, errormsg)
        if (k[0] == '-') or (k[len(k) - 1] == '-'):
            return False
    if len(name) > 128:
        return False
    # Добавляем в список корректных символов . ; " ! : ,
    correctchrlist.extend([ord('.'), ord(';'), ord('"')])
    onlyinquoteschrlist = [ord('!'), ord(','), ord(':')]
    correctchrlist.extend(onlyinquoteschrlist)
    # Проверка на парные кавычки
    if name.count('"') % 2 != 0:
        return False
    # Переменные для отслеживания точки и открывающихся кавычек
    doubledot = False
    inquotes = False
    for k in name:
        if k == '"':
            inquotes = not inquotes
        if (ord(k) in onlyinquoteschrlist) and (inquotes == False):
            return False
        if ord(k) not in correctchrlist:
            errormsg = "Недопустимый символ " + k
            return False
        # проверка на две точки подряд
        if k == '.':
            if doubledot:
                return False
            else:
                doubledot = True
    return True


def log(message=None, where='ne napisal', full=False, comments="None"):
    """[
    :param message: class; ответ из тг(message_handler)
    :param where: str; место(имя функции) где вызывается эта функция
    :param full: True/False
    :param comments: str; хз, любой ваш коментарий
    :return: в консоль пишет лог
    """
    global count, history
    count += 1
    if history:
        history = False
        print("""\033[33mWriting history started:\033[30m""")
    elif full:
        try:
            print(f"""\033[33m{"-" * 100}
time: \033[36m{tconv(message.date)}\033[33m
log №{count}
from: {where}
full: {full}
id: \033[36m{message.from_user.id}\033[33m
username: \033[36m{message.from_user.username}\033[33m
first_name(имя): \033[36m{message.from_user.first_name}\033[33m
last_name(фамилия): \033[36m{message.from_user.last_name}\033[33m
text: {message.text}
message: \033[35m{message}\033[33m
comments: \033[31m{comments}\033[33m""")
        except Exception as er:
            print(f"""\033[31m{"-" * 100}\n!ошибка, лог №{count}\n message: {message}
where: {where}
full: {full}\033
comments: {comments}
error: {er}[0m""")
    else:
        try:
            print(f"""\033[33m{"-" * 100}
time: \033[36m{tconv(message.date)}\033[33m
log №{count}
from: {where}
full: {full}
id: \033[36m{message.from_user.id}\033[33m
username: \033[36m{message.from_user.username}\033[33m
first_name(имя): \033[36m{message.from_user.first_name}\033[33m
last_name(фамилия): \033[36m{message.from_user.last_name}\033[33m
text: \033[35m{message.text}\033[33m
comment: {comments}\033[0m""")
        except Exception as er:
            print(f"""\033[31m!ошибка! Лог №{count}\n message: {message}
time: \033[36m{datetime.datetime.now()}\033[33m
where: {where}
full: {full}
comments: {comments}
error: {er}\033[0m""")


def keyboard_creator(list_of_names, one_time=True):
    """
    :param list_of_names: list; это список с именами кнопок(['1', '2'] будет каждая кнопка в ряд)
    [['1', '2'], '3'] первые 2 кнопки будут на 1 линии, а 3 снизу)
    :param one_time: bool; скрыть клаву после нажатия или нет
    :return: готовый класс клавиатуры в низу экрана
    """
    returned_k = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    for i in list_of_names:
        if isinstance(i, list):
            string = ""
            for o in range(len(i) - 1):
                string += f"'{i[o]}', "
            string += f"'{i[-1]}'"
            exec(f"""returned_k.row({string})""")
            continue
        exec(f"""returned_k.row('{i}')""")
    return returned_k


def buttons_creator(dict_of_names, how_many_rows=8):
    """
    :param dict_of_names: dict; это словарь, первые ключи могут быть любыми, они разделяют кнопки на ряды, а значениями этих ключей
           являются другие словари. Первый их аргумент это текст кнопки, а 2 это callback_data(то что будет передаваться в
           коллбек). Например: {
                                   '1': {
                                       'текст первой кнопки': 'нажали на кнопку 1',
                                       'текст второй кнопки': 'нажали на кнопку 2'
                                       },
                                   '2': {
                                       'текст третьей кнопки': 'нажали на кнопку 3'
                                       }
                               }
    :param how_many_rows: int; это максимальное количество кнопок в ряду
    :return: готовый класс кнопок под сообщением
    """
    returned_k = types.InlineKeyboardMarkup(row_width=how_many_rows)
    for i in dict_of_names.keys():
        if type(dict_of_names[i]) is dict:
            count = 0
            for o in dict_of_names[i].keys():
                count += 1
                exec(
                    f"""button{count} = types.InlineKeyboardButton(text='{o}', callback_data='{dict_of_names[i][o]}')""")
            s = []
            for p in range(1, count + 1):
                s.append(f"button{p}")
            exec(f"""returned_k.add({', '.join(s)})""")
        else:
            exec(f"""button = types.InlineKeyboardButton(text='{i}', callback_data='{dict_of_names[i]}')""")
            exec(f"""returned_k.add(button)""")
    return returned_k


def update(message):
    """
    :param message: class; ответ из тг(message_handler)
    """
    session = db_session.create_session()
    user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
    user.time = tconv(message.date)
    session.commit()


class Human:
    """
    супер пупер гениальная моя разработка
    Это класс без параметров, но их можно добавлять сколько угодно к каждому отдельному объекту.
    Например:
    a = Human(name="Влад")
    b = Human(name="Василь", teacher=True)
    """

    def __init__(self, **args):
        for i in args.keys():
            if type(args[i]) is str:
                exec(f"self.{i} = '{args[i]}'")
            else:
                exec(f"self.{i} = {args[i]}")


def clean_lower(line):
    """
    :param line: str; строка, из которой надо кикнуть все символы и в нижний регистр перевести
    :return: отворматированную строку
    """
    global jobs
    line = str(line).lower()
    line = re.sub(r"[\\\/\.\,\?\!@\"\'#№%^&\*\+\-;–:—\(\)\[\]\{\}\-_<>«»]", " ", line).split()
    new_line = []
    line = set(line)
    for key, value in SINONIMS.items():
        if len(line.intersection(value)) > 0:
            new_line.append(key)
    new_line.extend(list(line.intersection(jobs)))
    return list(set(new_line))


def search_workers(tg_id):
    try:
        list_of_peoples = []
        session = db_session.create_session()
        jobler = session.query(Ban).filter(Ban.tg_id == tg_id).first()
        request_of_jobs = clean_lower(jobler.arg1.lower())
        bosses = session.query(Boss).all()
        request_of_jobs = set(request_of_jobs).intersection(jobs)
        part_1 = []
        part_2 = []
        part_3 = []
        part_4 = []
        for i in bosses:
            print(i.tags)
            if len(request_of_jobs.intersection(set(i.tags.split()))) > 0:
                p = (len(request_of_jobs.intersection(set(i.tags.split())))) / (len(request_of_jobs))
                s = abs(int(jobler.arg3) - int(i.salary)) / 20000
                np1 = np.array([0, 0, 0, 0])
                np2 = np.array([0, 0, 0, 0])
                for hz in i.timetable.split():
                    if hz == "Стажировка":
                        np2[0] = 1
                    elif hz == "Проектная работа":
                        np2[1] = 1
                    elif hz == "Частичная занятость":
                        np2[2] = 1
                    elif hz == "Полная занятость":
                        np2[3] = 1
                    elif hz == "Все варианты":
                        np2 = np.array([1, 1, 1, 1])
                if jobler.arg2 == "Стажировка":
                    np1[0] = 1
                elif jobler.arg2 == "Проектная работа":
                    np1[1] = 1
                elif jobler.arg2 == "Частичная занятость":
                    np1[2] = 1
                elif jobler.arg2 == "Полная занятость":
                    np1[3] = 1
                elif jobler.arg2 == "Все варианты":
                    np1 = np.array([1, 1, 1, 1])
                if any(list(np1 * np2)):
                    e = 1
                else:
                    e = 0.8
                if i.salary <= int(jobler.arg3):
                    r = p + e - s
                else:
                    r = p + e + s
                if p >= 0.75:
                    part_1.append(Human(id=i.id, job=i.name_of_vacancy, salary=i.salary, r=r))
                elif p >= 0.5:
                    part_2.append(Human(id=i.id, job=i.name_of_vacancy, salary=i.salary, r=r))
                elif p >= 0.25:
                    part_3.append(Human(id=i.id, job=i.name_of_vacancy, salary=i.salary, r=r))
                elif p >= 0:
                    part_4.append(Human(id=i.id, job=i.name_of_vacancy, salary=i.salary, r=r))
                else:
                    log(message=None, where="махинации с поиском в распределении по группам", full=False,
                        comments=f"p = {p}")
        part_1.sort(key=lambda x: -x.r)
        part_2.sort(key=lambda x: -x.r)
        part_3.sort(key=lambda x: -x.r)
        part_4.sort(key=lambda x: -x.r)
        list_of_peoples.extend(part_1)
        list_of_peoples.extend(part_2)
        list_of_peoples.extend(part_3)
        list_of_peoples.extend(part_4)
        return list_of_peoples
    except Exception as ex:
        log(full=True, where="search_workers", comments=str(ex))


def search(tg_id=-1):
    """
    :param tg_id: int; тг id человека который ввёл параметры запроса
    :return: list; список из моих гениальных классов(Human())
    """
    try:
        list_of_peoples = []
        if tg_id == -1:
            session = db_session.create_session()
            users = session.query(People).all()
            for i in users:
                list_of_peoples.append(Human(id=i.id, job=i.job, salary=i.salary))
            return list_of_peoples
        else:
            session = db_session.create_session()
            jobler = session.query(Ban).filter(Ban.tg_id == tg_id).first()
            request_of_jobs = clean_lower(jobler.arg1.lower())
            users = session.query(People).all()
            request_of_jobs = set(request_of_jobs).intersection(jobs)
            part_1 = []
            part_2 = []
            part_3 = []
            part_4 = []
            for i in users:
                if len(request_of_jobs.intersection(set(i.tags.split()))) > 0:
                    p = (len(request_of_jobs.intersection(set(i.tags.split())))) / (len(request_of_jobs))
                    s = abs(int(jobler.arg3) - int(i.salary)) / 20000
                    np1 = np.array([0, 0, 0, 0])
                    np2 = np.array([0, 0, 0, 0])
                    for hz in i.employment.split():
                        if hz == "Стажировка":
                            np2[0] = 1
                        elif hz == "Проектная работа":
                            np2[1] = 1
                        elif hz == "Частичная занятость":
                            np2[2] = 1
                        elif hz == "Полная занятость":
                            np2[3] = 1
                        elif hz == "Все варианты":
                            np2 = np.array([1, 1, 1, 1])
                    if jobler.arg2 == "Стажировка":
                        np1[0] = 1
                    elif jobler.arg2 == "Проектная работа":
                        np1[1] = 1
                    elif jobler.arg2 == "Частичная занятость":
                        np1[2] = 1
                    elif jobler.arg2 == "Полная занятость":
                        np1[3] = 1
                    elif jobler.arg2 == "Все варианты":
                        np1 = np.array([1, 1, 1, 1])
                    if any(list(np1 * np2)):
                        e = 1
                    else:
                        e = 0.8
                    if i.salary <= int(jobler.arg3):
                        r = p + e + s
                    else:
                        r = p + e - s
                    if p >= 0.75:
                        part_1.append(Human(id=i.id, job=i.job, salary=i.salary, r=r))
                    elif p >= 0.5:
                        part_2.append(Human(id=i.id, job=i.job, salary=i.salary, r=r))
                    elif p >= 0.25:
                        part_3.append(Human(id=i.id, job=i.job, salary=i.salary, r=r))
                    elif p >= 0:
                        part_4.append(Human(id=i.id, job=i.job, salary=i.salary, r=r))
                    else:
                        log(message=None, where="махинации с поиском в распределении по группам", full=False,
                            comments=f"p = {p}")
            part_1.sort(key=lambda x: -x.r)
            part_2.sort(key=lambda x: -x.r)
            part_3.sort(key=lambda x: -x.r)
            part_4.sort(key=lambda x: -x.r)
            list_of_peoples.extend(part_1)
            list_of_peoples.extend(part_2)
            list_of_peoples.extend(part_3)
            list_of_peoples.extend(part_4)
            return list_of_peoples
    except Exception as ex:
        log(full=True, where="search", comments=str(ex))


def pdf(user_id):
    """
    создание пдф, это делал Василь, так что я хз
    :param user_id: int; номер челика из таблицы people
    """
    try:
        file = open('data/media/pdf.html', mode="w", encoding="utf-8")
    except Exception:
        file = open('/home/AVI2005/TelgrammBot/data/media/pdf.html', mode="w", encoding="utf-8")
    session = db_session.create_session()
    user = session.query(People).filter(People.id == user_id).first()
    text = f"""<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <img src="icon.png" style="float:left; height: 150px;">
    <div style="margin-left: 900px; padding-top: 1px; width: 500px;">
        <h2 style="font-family: Arial;">Школа программирования Тюменской области</h2>
        <h3></h3>
        <h3><a href="https://tmn-it.ru/shkola-programmirovaniya/code@tmn-it.ru">https://tmn-it.ru/shkola-programmirovaniya/
            code@tmn-it.ru</a>
        </h3>
    </div>
    <h1 style="font-size: 40px; margin-top: 120px;" align="center">Резюме</h1>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">ФИО</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.name}</p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">Желаемая работа</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.job}</p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">Дата рождения</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.birth_date}</p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">Номер телефона</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.phone}</p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">Адрес электронной почты</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.mail}</p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">Местожительство</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.city}</p>
    <p style="margin-top: 100px; display: inline-block; width: 1300px;"></p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">Форма занятости</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.schedule}</p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">Ожидаемая заработная плата</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.salary}</p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">Опыт работы</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.experience}</p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">Профессиональные достижения</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.achievements}</p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">Образование</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.education}</p>
    <h1 style="vertical-align: top; display: inline-block; width: 300px; margin-left: 60px;">О себе</h1>
    <p style="display: inline-block; width: 900px; margin-left: 40px; font-size: 32px; text-align: justify;">{user.about_me}</p>
    </body>
    </html>"""
    for i in text.split("\n"):
        file.write(i + "\n")
    file.close()
    # client = pdfcrowd.HtmlToPdfClient("AVI2005", "5ec73c962bac1db58b3e27d9dd183a86")
    # client.setPageWidth("1400px")
    # client.setPageHeight("2000px")
    # client.convertFileToFile("data/media/pdf.html", 'data/media/resume.pdf')
    path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    from_file("data/media/pdf.html", 'data/media/resume.pdf', configuration=config)


def have_vacancy(message):
    session = db_session.create_session()
    user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
    try:
        if user.ban and user.count == 0:
            # video = open("data/media/БАН.mp4", "rb")
            bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
                             reply_markup=types.ReplyKeyboardRemove())
            # bot.send_video(message.from_user.id, video)
            user.count += 1
            session.commit()
            return bot.register_next_step_handler(message, get_text_messages)
        elif user.ban and user.count != 0:
            return bot.register_next_step_handler(message, get_text_messages)
    except Exception:
        user = Ban()
        user.tg_id = message.from_user.id
        user.ban = False
        user.count = 0
        session.add(user)
        session.commit()
    update(message)
    log(message=message, where="get_text_messages")
    keyboard = keyboard_creator([["Поиск работника", "Поиск работы"],
                                 "Оставить вакансию", "Оставить резюме",
                                 "Запись на обучение в ШП"])
    user_like_boss = session.query(Boss).filter(Boss.tg_id == message.from_user.id).first()
    user_like_people = session.query(People).filter(People.tg_id == message.from_user.id).first()
    hz = 0
    try:
        if user_like_people.phone:
            hz += 1
    except Exception:
        pass
    try:
        if user_like_boss.phone:
            hz += 1
    except Exception:
        pass
    if hz > 0:
        bot.send_message(message.from_user.id, f"Здраствуйте")
        list_of_buttons = [["Поиск работника", "Поиск работы"],
                           "Запись на обучение"]
        try:
            if len(user_like_people.liked) > 0:
                list_of_buttons.insert(1, ["Избранные вакансии", "Очистить список вакансии"])
        except Exception:
            pass
        try:
            if len(user_like_boss.liked) > 0:
                list_of_buttons.insert(1, ["Избранные резюме", "Очистить список резюме"])
        except Exception:
            pass
        aboba = []
        try:
            if user_like_people.phone:
                aboba.append(["Мое резюме", "Удалить резюме"])
        except Exception:
            aboba.append("Оставить резюме")
        try:
            if user_like_boss.phone:
                aboba.append(["Мои вакансии", "" if user_like_boss.spratan else "Скрыть вакансию"])
        except Exception:
            aboba.append("Оставить вакансию")
        for i in aboba:
            list_of_buttons.insert(1, i)
        keyboard = keyboard_creator(list_of_buttons)
        bot.send_message(message.from_user.id, f"Вы в главном меню", reply_markup=keyboard)
        return bot.register_next_step_handler(message, main_menu)
    bot.send_message(message.from_user.id, f"Здраствуйте")
    bot.send_message(message.from_user.id, f"Что вас интересует?", reply_markup=keyboard)
    return bot.register_next_step_handler(message, vilka)


def liked(tg_id, who=0):
    _list = []
    session = db_session.create_session()
    if who:
        chelik = session.query(Boss).filter(Boss.tg_id == tg_id).first()
    else:
        chelik = session.query(People).filter(People.tg_id == tg_id).first()
    list_of_liked = chelik.liked.split(",")
    for tg_id_liked in list_of_liked:
        tg_id_liked = int(tg_id_liked)
        if who:
            dodik = session.query(People).filter(People.tg_id == tg_id_liked).first()
            _list.append(Human(id=dodik.id, job=dodik.job, salary=dodik.salary))
        else:
            dodik = session.query(Boss).filter(Boss.tg_id == tg_id_liked).first()
            _list.append(Human(id=dodik.id, job=dodik.name_of_vacancy, salary=dodik.salary))
    return _list


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """
    принимает все сообщения если функция никуда не переадресовала в другую
    :param message: class, тг возращает
    :return: переход в vilka(message)
    """
    try:
        return have_vacancy(message)
    except Exception as er:
        log(message=message, where="get_text_messages", comments=str(er))


def vilka(message):
    """
    выбор ветки
    :param message: class; тг возвращает
    :return: переход дальше по ветке, либо переход в саму в себя
    """
    try:
        log(message=message, where="vilka")
        keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
        try:
            if user.ban and user.count == 0:
                video = open("data/media/БАН.mp4", "rb")
                bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_video(message.from_user.id, video)
                user.count += 1
                session.commit()
                return bot.register_next_step_handler(message, get_text_messages)
            elif user.ban and user.count != 0:
                return bot.register_next_step_handler(message, get_text_messages)
        except Exception:
            user = Ban()
            user.tg_id = message.from_user.id
            user.ban = False
            user.count = 0
            # user.time = tconv(message.date)
            session.add(user)
            session.commit()
        update(message)
        if message.text == "\\start":
            return have_vacancy(message)
        elif message.text == "Поиск работника":
            bot.send_message(message.from_user.id,
                             f"Какая у вас вакансия? Введите название должности, основной стек через пробелы",
                             reply_markup=keyboard)
            return bot.register_next_step_handler(message, staks)
        elif message.text == "Поиск работы":
            bot.send_message(message.from_user.id,
                             f"Кем вы хотите работать? Введите название должности, основной стек через пробелы",
                             reply_markup=keyboard)
            return bot.register_next_step_handler(message, staks, who=1)
        elif message.text == "Оставить вакансию":
            bot.send_message(message.from_user.id,
                             f"Наименование организации",
                             reply_markup=keyboard)
            return bot.register_next_step_handler(message, start_creating_vacancy)
        elif message.text == "Оставить резюме":
            bot.send_message(message.from_user.id,
                             f"ФИО",
                             reply_markup=keyboard)
            return bot.register_next_step_handler(message, start_creating_tender)
        elif message.text == "Запись на обучение в ШП":
            bot.send_message(message.from_user.id,
                             f"Эта функция в находится разработке. Выберите другой вариант в меню.")
            return bot.register_next_step_handler(message, vilka)
        # elif message.text == "Расписание обучения":
        #     bot.send_message(message.from_user.id,
        #                      f"Эта функция в находится разработке. Выберите другой вариант в меню.")
        #     return bot.register_next_step_handler(message, vilka)
        else:
            bot.send_message(message.from_user.id, f"Извините, но такого варианта нет.")
            return bot.register_next_step_handler(message, vilka)
    except Exception as er:
        log(message=message, full=True, where="vilka", comments=str(er))


def start_creating_vacancy(message):
    try:
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
        keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
        try:
            if user.ban and user.count == 0:
                video = open("data/media/БАН.mp4", "rb")
                bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_video(message.from_user.id, video)
                user.count += 1
                session.commit()
                return bot.register_next_step_handler(message, get_text_messages)
            elif user.ban and user.count != 0:
                return bot.register_next_step_handler(message, get_text_messages)
        except Exception:
            user = Ban()
            user.tg_id = message.from_user.id
            user.ban = False
            user.count = 0
            # user.time = tconv(message.date)
            session.add(user)
            session.commit()
        update(message)
        if message.text in [f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню", "\\start"]:

            return have_vacancy(message)
        else:
            bos = Boss()
            bos.name_of_company = message.text
            bos.tg_id = message.from_user.id
            bos.liked = ""
            bos.phone = ""
            bos.email = ""
            bos.city = ""
            bos.name_of_vacancy = ""
            bos.zadachi_funkcii = ""
            bos.type = ''
            bos.about_company = ''
            bos.job_of_rab = ''
            bos.trebovanija = ""
            bos.spratan = False
            bos.timetable = ""
            bos.tags = ""
            bos.salary = 0
            bos.count = 1
            session.add(bos)
            session.commit()
            bot.send_message(message.from_user.id, f"Наименование вакансии", reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_vacancy)
    except Exception as er:
        print(er)


def start_creating_tender(message):
    try:
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
        keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
        try:
            if user.ban and user.count == 0:
                video = open("data/media/БАН.mp4", "rb")
                bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_video(message.from_user.id, video)
                user.count += 1
                session.commit()
                return bot.register_next_step_handler(message, get_text_messages)
            elif user.ban and user.count != 0:
                return bot.register_next_step_handler(message, get_text_messages)
        except Exception:
            user = Ban()
            user.tg_id = message.from_user.id
            user.ban = False
            user.count = 0
            # user.time = tconv(message.date)
            session.add(user)
            session.commit()
        update(message)
        if message.text in [f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню", "\\start"]:
            return have_vacancy(message)
        else:
            bos = People()
            bos.tg_id = message.from_user.id
            bos.name_of_company = message.text
            bos.count = 1
            session.add(bos)
            session.commit()
            bot.send_message(message.from_user.id, f"Дата рождени в формате дд.мм.гггг", reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_tender)
    except Exception as er:
        print(er)


def creating_vacancy(message):
    try:
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
        keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
        try:
            if user.ban and user.count == 0:
                video = open("data/media/БАН.mp4", "rb")
                bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_video(message.from_user.id, video)
                user.count += 1
                session.commit()
                return bot.register_next_step_handler(message, get_text_messages)
            elif user.ban and user.count != 0:
                return bot.register_next_step_handler(message, get_text_messages)
        except Exception:
            user = Ban()
            user.tg_id = message.from_user.id
            user.ban = False
            user.count = 0
            # user.time = tconv(message.date)
            session.add(user)
            session.commit()
        update(message)
        user = session.query(Boss).filter(Boss.tg_id == message.from_user.id).first()
        if message.text in [f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню", "\\start"]:
            session.delete(user)
            session.commit()
            return have_vacancy(message)
        elif user.count == 1:
            user.name_of_vacancy = message.text
            user.count += 1
            session.commit()
            keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
            bot.send_message(message.from_user.id, f"Требования к сотруднику", reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 2:
            user.trebovanija = message.text
            user.count += 1
            session.commit()
            keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
            bot.send_message(message.from_user.id, f"Задачи и функции", reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 3:
            user.zadachi_funkcii = message.text
            user.count += 1
            session.commit()
            keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
            bot.send_message(message.from_user.id, f"Заработная плата", reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 4:
            govnolist = re.findall(r"\b\d+k*\b", str(message.text).replace("к", "k"))
            govnolist = [str(i).replace("k", "000") for i in govnolist]
            govnolist = list(map(int, govnolist))
            if not govnolist:
                keyboard = keyboard_creator([f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"Вы не ввели ЗП, попробуйте ещё раз.", reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
            user.salary = sum(govnolist) / len(govnolist)
            user.count += 1
            session.commit()
            keyboard = keyboard_creator(
                ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость", "Все варианты",
                 f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
            bot.send_message(message.from_user.id, f"Тип занятости",
                             reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 5:
            if message.text in ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость",
                                "Все варианты"]:
                user.count += 1
                user.type = message.text
                session.commit()
                keyboard = keyboard_creator(["Гибкий график", "Полный день", "Удаленная работа",
                     f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"График",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
            else:
                keyboard = keyboard_creator(
                    ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость", "Все варианты",
                     f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"К сожалению нет такого варианта, попробуйте другой вариант.",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 6:
            if message.text in ["Гибкий график", "Полный день", "Удаленная работа"]:
                user.count += 1
                user.timetable = message.text
                session.commit()
                bot.send_message(message.from_user.id, f"Расскажите о вашей компании",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
            else:
                keyboard = keyboard_creator(["Гибкий график", "Полный день", "Удаленная работа",
                                             f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"К сожалению нет такого варианта, попробуйте другой вариант.",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 7:
            user.about_company = message.text
            user.count += 1
            session.commit()
            keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
            bot.send_message(message.from_user.id, f"ФИО контактного лица", reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 8:
            user.name_of_rab = message.text
            user.count += 1
            session.commit()
            keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
            bot.send_message(message.from_user.id, f"Телефон", reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 9:
            phone = ""
            for i in message.text:
                if i.isdigit():
                    phone += i
            if len(phone) == 11:
                user.phone = phone
                user.count += 1
                session.commit()
                keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"Email",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)

            else:
                bot.send_message(message.from_user.id, f"Вы ввели не правильный номер телефона.", reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 10:
            email = message.text.replace(" ", "")
            if correctemail(email):
                user.email = email
                user.count = 0

                session.commit()
                user_like_boss = session.query(Boss).filter(Boss.tg_id == message.from_user.id).first()
                user_like_people = session.query(People).filter(People.tg_id == message.from_user.id).first()
                list_of_buttons = [["Поиск работника", "Поиск работы"],
                                   "Запись на обучение",
                                   "Удалить всю информацию о себе"]
                try:
                    if len(user_like_people.liked) > 0:
                        list_of_buttons.insert(1, ["Посмотреть избранных работников", "Очистить список"])
                except Exception:
                    pass
                try:
                    if len(user_like_boss.liked) > 0:
                        list_of_buttons.insert(1, ["Посмотреть избранные работы", "Очистить список"])
                except Exception:
                    pass
                aboba = []
                try:
                    if user_like_people.phone:
                        aboba.append(["Мое резюме"])
                except Exception:
                    aboba.append("Создать резюме работника")
                try:
                    if user_like_boss.phone:
                        aboba.append(["Мои вакансии"])
                except Exception:
                    aboba.append("Создать вакансию")
                for i in aboba:
                    list_of_buttons.insert(1, i)
                keyboard = keyboard_creator(list_of_buttons)
                bot.send_message(message.from_user.id, f"Ваша вакансия создана. Вы можете посмотреть список своих вакансий нажав на кнопку \"Мои вакансии\"Вы были переведены в главное меню", reply_markup=keyboard)
                return bot.register_next_step_handler(message, main_menu)
            else:
                bot.send_message(message.from_user.id, f"Вы ввели не правильный email.", reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
    except Exception as er:
        print(er)


def creating_tender(message):
    try:
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
        keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
        try:
            if user.ban and user.count == 0:
                video = open("data/media/БАН.mp4", "rb")
                bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_video(message.from_user.id, video)
                user.count += 1
                session.commit()
                return bot.register_next_step_handler(message, get_text_messages)
            elif user.ban and user.count != 0:
                return bot.register_next_step_handler(message, get_text_messages)
        except Exception:
            user = Ban()
            user.tg_id = message.from_user.id
            user.ban = False
            user.count = 0
            # user.time = tconv(message.date)
            session.add(user)
            session.commit()
        update(message)
        user = session.query(People).filter(People.tg_id == message.from_user.id).first()
        if message.text in [f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню", "\\start"]:
            session.delete(user)
            session.commit()
            return have_vacancy(message)
        elif user.count == 1:
            user.about_me = message.text
            user.count += 1
            session.commit()
            bot.send_message(message.from_user.id, f"Введите номер телефона")
            return bot.register_next_step_handler(message, creating_tender)
        elif user.count == 2:
            phone = ""
            for i in message.text:
                if i.isdigit():
                    phone += i
            if len(phone) == 11:
                user.phone = phone
                user.count += 1
                session.commit()
                bot.send_message(message.from_user.id, f"Введите свой email")
                return bot.register_next_step_handler(message, creating_tender)
            else:
                bot.send_message(message.from_user.id, f"Вы ввели не правильный номер телефона", reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_tender)
        elif user.count == 3:
            email = message.text.replace(" ", "")
            if correctemail(email):
                user.email = email
                user.count += 1
                session.commit()
                bot.send_message(message.from_user.id, f"Введите город, в котором вы живете",
                                 reply_markup=types.ReplyKeyboardRemove())
                return bot.register_next_step_handler(message, creating_tender)
            else:
                bot.send_message(message.from_user.id, f"Вы ввели не правильный email", reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_tender)
        elif user.count == 4:
            user.city = str(message.text)
            user.count += 1
            session.commit()
            bot.send_message(message.from_user.id, f"Желаемая работа (название вакансии, сфера или направление работы)",
                             reply_markup=types.ReplyKeyboardRemove())
            return bot.register_next_step_handler(message, creating_tender)
        elif user.count == 5:
            user.count += 1
            session.commit()
            list_of_jobs = str(message.text).replace(";", " ").replace("/", " ").replace(
                "|", " ").replace("~", " ").replace(":", " ").replace("{", " ").replace("}", " ").replace("[",
                                                                                                          " ").replace(
                "]", " ").replace("+", " ").replace("-", " ")
            # nekotorie mohinacii c vvodom
            user.job = ", ".join(list_of_jobs.split())
            shit = []
            for i in list_of_jobs:
                for key in SINONIMS.keys():
                    if i in SINONIMS[key]:
                        shit.append(key)
                        break
                else:
                    if i in jobs:
                        shit.append(i)
            user.tags = " ".join(shit)
            session.commit()
            bot.send_message(message.from_user.id, f"Ожидаемая заработная плата",
                             reply_markup=types.ReplyKeyboardRemove())
            return bot.register_next_step_handler(message, creating_tender)
        elif user.count == 6:
            govnolist = re.findall(r"\b\d+k*\b", str(message.text).replace("к", "k"))
            govnolist = [str(i).replace("k", "000") for i in govnolist]
            govnolist = list(map(int, govnolist))
            if not govnolist:
                keyboard = keyboard_creator([f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"Вы не ввели зарабтную плату, попробуйте ещё раз", reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
            user.salary = sum(govnolist) / len(govnolist)
            user.count += 1
            session.commit()
            keyboard = keyboard_creator(
                ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость", "Все варианты",
                 f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
            bot.send_message(message.from_user.id, f"Занятость (выберите подходящий вариант",
                             reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_tender)
        elif user.count == 7:
            if message.text in ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость",
                                "Все варианты"]:
                user.count += 1
                user.employment = message.text
                session.commit()
                keyboard = keyboard_creator(
                    ["Гибкий график", "Полный день", "Удаленная работа",
                     f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id,
                                 f"Выберите желаемый график работы(Удаленная работа, Гибкий график и т.д.)",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_tender)
            else:
                keyboard = keyboard_creator(
                    ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость", "Все варианты",
                     f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"К сожалению нет такого варианта, попробуйте другой вариант",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 8:
            if message.text in ["Гибкий график", "Полный день", "Удаленная работа"]:
                user.count += 1
                user.schedule = message.text
                session.commit()
                bot.send_message(message.from_user.id,
                                 f"Опыт работы",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_tender)
            else:
                keyboard = keyboard_creator(
                    ["Гибкий график", "Полный день", "Удаленная работа", f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"К сожалению нет такого варианта, попробуйте другой вариант",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 9:
            user.count += 1
            user.experience = message.text
            session.commit()
            bot.send_message(message.from_user.id, f"Ваши профессиональные достижения",
                             reply_markup=types.ReplyKeyboardRemove())
            return bot.register_next_step_handler(message, creating_tender)
        elif user.count == 10:
            user.count += 1
            user.achievements = message.text
            session.commit()
            bot.send_message(message.from_user.id, f"Ваше образование",
                             reply_markup=types.ReplyKeyboardRemove())
            return bot.register_next_step_handler(message, creating_tender)
        elif user.count == 11:
            user.count += 1
            user.education = message.text
            session.commit()
            bot.send_message(message.from_user.id, f"Расскажите о себе", reply_markup=types.ReplyKeyboardRemove())
            return bot.register_next_step_handler(message, creating_tender)
        elif user.count == 12:
            user.count = 0
            user.about_me = message.text
            session.commit()
            user_like_boss = session.query(Boss).filter(Boss.tg_id == message.from_user.id).first()
            user_like_people = session.query(People).filter(People.tg_id == message.from_user.id).first()
            list_of_buttons = [["Поиск работника", "Поиск работы"],
                               "Запись на обучение"]
            try:
                if len(user_like_people.liked) > 0:
                    list_of_buttons.insert(1, ["Избранные вакансии", "Очистить список вакансии"])
            except Exception:
                pass
            try:
                if len(user_like_boss.liked) > 0:
                    list_of_buttons.insert(1, ["Избранные резюме", "Очистить список резюме"])
            except Exception:
                pass
            aboba = []
            try:
                if user_like_people.phone:
                    aboba.append(["Мое резюме"])
            except Exception:
                aboba.append("Оставить резюме")
            try:
                if user_like_boss.phone:
                    aboba.append(["Мои вакансии"])
            except Exception:
                aboba.append("Оставить вакансию")
            for i in aboba:
                list_of_buttons.insert(1, i)
            keyboard = keyboard_creator(list_of_buttons)
            bot.send_message(message.from_user.id, f"Ваше резюме зарегистрировано. Вы можете посмотреть резюме, нажав на кнопку \"Мое резюме\" . Вы были переведены в главное меню.", reply_markup=keyboard)
            return bot.register_next_step_handler(message, main_menu)
    except Exception as er:
        print(er)


def staks(message, who=0):
    """
    ввод тегов для поиска
    :param message: class, тг возвращает
    :return: переход в employment(message)
    """
    try:
        log(message=message, where="staks")
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
        try:
            if user.ban and user.count == 0:
                video = open("data/media/БАН.mp4", "rb")
                bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_video(message.from_user.id, video)
                user.count += 1
                session.commit()
                session.close()
                return bot.register_next_step_handler(message, get_text_messages)
            elif user.ban and user.count != 0:
                return bot.register_next_step_handler(message, get_text_messages)
        except Exception:
            user = Ban()
            user.tg_id = message.from_user.id
            user.ban = False
            user.count = 0
            # user.time = tconv(message.date)
            session.add(user)
            session.commit()
            session.close()
        update(message)
        keyboard = keyboard_creator([["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
                                     "Расписание обучения"])
        if message.text in ["\\start", f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"]:
            return have_vacancy(message)
        else:
            list_of_jobs = str(message.text).replace(";", " ").replace("/", " ").replace(
                "|", " ").replace("~", " ").replace(":", " ").replace("{", " ").replace("}", " ").replace("[",
                                                                                                          " ").replace(
                "]", " ").replace("+", " ").replace("-", " ")
            # nekotorie mohinacii c vvodom
            session = db_session.create_session()
            user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
            user.arg1 = list_of_jobs
            session.commit()
            session.close()
            keyboard = keyboard_creator(
                ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость", "Все варианты",
                 f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
            bot.send_message(message.from_user.id, f"Что вы предлагаете?", reply_markup=keyboard)
            return bot.register_next_step_handler(message, employment, who)
    except Exception as er:
        log(message=message, full=True, where="staks", comments=str(er))


def employment(message, who=0):
    """
    выбор занятости для поиска
    :param message: class; тг возращает
    :return: переход в salary(message)
    """
    try:
        log(message=message, where="employment")
        keyboard = keyboard_creator(
            ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость", "Все варианты",
             f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
        try:
            if user.ban and user.count == 0:
                video = open("data/media/БАН.mp4", "rb")
                bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_video(message.from_user.id, video)
                user.count += 1
                session.commit()
                session.close()
                return bot.register_next_step_handler(message, get_text_messages)
            elif user.ban and user.ban and user.count != 0:
                return bot.register_next_step_handler(message, get_text_messages)
        except Exception:
            user = Ban()
            user.tg_id = message.from_user.id
            user.ban = False
            user.count = 0
            # user.time = tconv(message.date)
            session.add(user)
            session.commit()
            session.close()
        update(message)
        if message.text in [f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню", "\\start"]:
            return have_vacancy(message)
        else:
            if message.text == "Стажировка":
                pass
            elif message.text == "Проектная работа":
                pass
            elif message.text == "Частичная занятость":
                pass
            elif message.text == "Полная занятость":
                pass
            elif message.text == "Все варианты":
                pass
            else:
                bot.send_message(message.from_user.id, f"Извините, но такого варианта нет.")
                return bot.register_next_step_handler(message, employment)
            keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
            session = db_session.create_session()
            user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
            user.arg2 = message.text
            session.commit()
            session.close()
            bot.send_message(message.from_user.id, f"Введите примерную зарплату в рублях:", reply_markup=keyboard)
            return bot.register_next_step_handler(message, salary, who)
    except Exception as er:
        log(message=message, full=True, where="employment", comments=str(er))


def salary(message, who=0):
    """
    ввод зарплаты для поиска, например(20000/20к/20k)
    :param message: class; тг возвращает
    :return: отправка отсортированного списка и переход в exit_to_vilka(message)
    """
    try:
        log(message=message, where="salary")
        keyboard = keyboard_creator([["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
                                     "Расписание обучения"])
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
        try:
            if user.ban and user.count == 0:
                video = open("data/media/БАН.mp4", "rb")
                bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_video(message.from_user.id, video)
                user.count += 1
                session.commit()
                return bot.register_next_step_handler(message, get_text_messages)
            elif user.ban and user.count != 0:
                return bot.register_next_step_handler(message, get_text_messages)
        except Exception:
            user = Ban()
            user.tg_id = message.from_user.id
            user.ban = False
            user.count = 0
            # user.time = tconv(message.date)
            session.add(user)
            session.commit()
        update(message)
        if message.text in [f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню", "\\start"]:
            return have_vacancy(message)
        else:
            govnolist = re.findall(r"\b\d+k*\b", str(message.text).replace("к", "k"))
            govnolist = [str(i).replace("k", "000") for i in govnolist]
            govnolist = list(map(int, govnolist))
            print(govnolist)
            if not govnolist:
                keyboard = keyboard_creator([f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"Вы не ввели ЗП, попробуйте ещё раз.", reply_markup=keyboard)
                return bot.register_next_step_handler(message, salary)
            bot.send_message(message.from_user.id, f"Начинаем поиск")
            user.arg3 = sum(govnolist) / len(govnolist)
            session.commit()
            if who:
                list_poiska = search_workers(message.from_user.id)
            else:
                list_poiska = search(message.from_user.id)
            if len(list_poiska) != 0:
                if who:
                    key_dict = {'1': {}}
                    if len(list_poiska) > 5:
                        key_dict["1"]["<"] = "back_boss"
                    text = f"Страница 1 из {len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1}\n\n"
                    _list = []
                    for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                        string = f"{1 + i}. {list_poiska[i].job}\n{list_poiska[i].salary} р."
                        _list.append(string)
                    text += "\n".join(_list)
                    for i in range(1, len(_list) + 1):
                        key_dict["1"][f"{i}"] = f"{i} boss"
                    if len(list_poiska) > 5:
                        key_dict["1"][">"] = "next_boss"
                    bot.send_message(message.from_user.id, text, reply_markup=buttons_creator(key_dict))
                else:
                    key_dict = {'1': {}}
                    if len(list_poiska) > 5:
                        key_dict["1"]["<"] = "back"
                    text = f"Страница 1 из {len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1}\n\n"
                    _list = []
                    for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                        string = f"{1 + i}. {list_poiska[i].job}\n{list_poiska[i].salary} р."
                        _list.append(string)
                    text += "\n".join(_list)
                    for i in range(1, len(_list) + 1):
                        key_dict["1"][f"{i}"] = f"{i} rab"
                    if len(list_poiska) > 5:
                        key_dict["1"][">"] = "next"
                    bot.send_message(message.from_user.id, text, reply_markup=buttons_creator(key_dict))
            else:
                text = "По вашему запросу ничего не найдено"
                bot.send_message(message.from_user.id, text)
                keyboard = keyboard_creator(
                    [["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
                     "Расписание обучения"])
                bot.send_message(message.from_user.id, f"Что вас интересует?", reply_markup=keyboard)
                return bot.register_next_step_handler(message, vilka)
            return bot.register_next_step_handler(message, exit_to_vilka)
            # return bot.register_next_step_handler(message, vilka, list_poiska)
    except Exception as er:
        log(message=message, full=True, where="salary", comments=str(er))


def exit_to_vilka(message):
    """
    хз шо это
    :param message: class; тг возвращает
    :return: переход в vilka(message)
    """
    try:
        log(message=message, where="exit_to_vilka")
        if message.text in [f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню", "\\start"]:
            return have_vacancy(message)
        return bot.register_next_step_handler(message, exit_to_vilka)
    except Exception as er:
        log(message=message, full=True, where="exit_to_vilka", comments=str(er))


def main_menu(message):
    """
    не рабает, в разработке
    :param message: class; тг возвращает
    :return: ничего
    """
    session = db_session.create_session()
    user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
    try:
        if user.ban and user.count == 0:
            video = open("data/media/БАН.mp4", "rb")
            bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
                             reply_markup=types.ReplyKeyboardRemove())
            bot.send_video(message.from_user.id, video)
            user.count += 1
            session.commit()
            return bot.register_next_step_handler(message, get_text_messages)
        elif user.ban and user.count != 0:
            return bot.register_next_step_handler(message, get_text_messages)
    except Exception:
        user = Ban()
        user.tg_id = message.from_user.id
        user.ban = False
        user.count = 0
        # user.time = tconv(message.date)
        session.add(user)
        session.commit()
    if message.text == "Удалить всю информацию о себе":
        user_like_boss = session.query(Boss).filter(Boss.tg_id == message.from_user.id).first()
        user_like_people = session.query(People).filter(People.tg_id == message.from_user.id).first()
        try:
            session.delete(user_like_boss)
        except Exception:
            pass
        try:
            session.delete(user_like_people)
        except Exception:
            pass
        session.commit()
        return have_vacancy(message)
    elif message.text == "Поиск работника":
        keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
        bot.send_message(message.from_user.id,
                         f"Какая у вас вакансия? Введите название должности, основной стек через пробелы",
                         reply_markup=keyboard)
        return bot.register_next_step_handler(message, staks)
    elif message.text == "Поиск работы":
        keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
        bot.send_message(message.from_user.id,
                         f"Кем вы хотите работать? Введите название должности, основной стек через пробелы",
                         reply_markup=keyboard)
        return bot.register_next_step_handler(message, staks, who=1)
    elif message.text == "Удалить резюме":
        user_like_people = session.query(People).filter(People.tg_id == message.from_user.id).first()
        session.delete(user_like_people)
        session.commit()
        return have_vacancy(message)
    elif message.text == "Удалить вакансию":
        user_like_boss = session.query(Boss).filter(Boss.tg_id == message.from_user.id).first()
        session.delete(user_like_boss)
        session.commit()
        return have_vacancy(message)
    elif message.text == "Мои вакансии":
        bot.send_message(message.from_user.id,
                         f"Эта функция в находится разработке. Выберите другой вариант в меню.")
        return bot.register_next_step_handler(message, main_menu)
    elif message.text == "Мое резюме":
        bot.send_message(message.from_user.id,
                         f"Эта функция в находится разработке. Выберите другой вариант в меню.")
        return bot.register_next_step_handler(message, main_menu)
    elif message.text == "Оставить вакансию":
        keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
        bot.send_message(message.from_user.id,
                         f"Наименование организации",
                         reply_markup=keyboard)
        return bot.register_next_step_handler(message, start_creating_vacancy)
    elif message.text == "Оставить резюме":
        keyboard = keyboard_creator([f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
        bot.send_message(message.from_user.id,
                         f"ФИО",
                         reply_markup=keyboard)
        return bot.register_next_step_handler(message, start_creating_tender)
    elif message.text == "Запись на обучение":
        bot.send_message(message.from_user.id,
                         f"Эта функция в находится разработке. Выберите другой вариант в меню.")
        return bot.register_next_step_handler(message, main_menu)
    elif message.text == "Избранные резюме":
        text = []
        _list = liked(message.from_user.id, 1)
        text.append(f"Страница 1 из {len(_list) // 5 if len(_list) % 5 == 0 else len(_list) // 5 + 1}")
        key_dict = {'1': {}}
        if len(_list) > 5:
            key_dict["1"]["<"] = "back_liked_boss"
        for gg in range(1, (6 if len(_list) >= 5 else len(_list) + 1)):
            key_dict["1"][f"{gg}"] = f"{gg} liked_boss"
        if len(_list) > 5:
            key_dict["1"][">"] = "next_liked_boss"
        text.append("")
        for i in range(5 if len(_list) >= 5 else len(_list) % 5):
            text.append(
                f"{1 + i}. {_list[i].job}\n{int(_list[i].salary)} р.")
        text = "\n".join(text)
        bot.send_message(message.from_user.id, text, reply_markup=buttons_creator(key_dict))
        return bot.register_next_step_handler(message, main_menu)
    elif message.text == "Избранные вакансии":
        text = []
        _list = liked(message.from_user.id)
        text.append(f"Страница 1 из {len(_list) // 5 if len(_list) % 5 == 0 else len(_list) // 5 + 1}")
        key_dict = {'1': {}}
        if len(_list) > 5:
            key_dict["1"]["<"] = "back_liked_rab"
        for gg in range(1, len(_list) + 1):
            key_dict["1"][f"{gg}"] = f"{gg} liked_rab"
        if len(_list) > 5:
            key_dict["1"][">"] = "next_liked_rab"
        text.append("")
        for i in range(5 if len(_list) >= 5 else len(_list) % 5):
            text.append(
                f"{1 + i}. {_list[i].job}\n{int(_list[i].salary)} р.")
        text = "\n".join(text)
        bot.send_message(message.from_user.id, text, reply_markup=buttons_creator(key_dict))
        return bot.register_next_step_handler(message, main_menu)
    elif message.text == "Очистить список резюме":
        session = db_session.create_session()
        chel = session.query(Boss).filter(Boss.tg_id == message.from_user.id).first()
        chel.liked = ""
        session.commit()
        user_like_boss = session.query(Boss).filter(Boss.tg_id == message.from_user.id).first()
        user_like_people = session.query(People).filter(People.tg_id == message.from_user.id).first()
        list_of_buttons = [["Поиск работника", "Поиск работы"],
                           "Запись на обучение",
                           "Удалить всю информацию о себе"]
        try:
            if len(user_like_people.liked) > 0:
                list_of_buttons.insert(1, ["Посмотреть избранных работников", "Очистить список"])
        except Exception:
            pass
        try:
            if len(user_like_boss.liked) > 0:
                list_of_buttons.insert(1, ["Посмотреть избранные вакансии", "Очистить список"])
        except Exception:
            pass
        aboba = []
        try:
            if user_like_people.phone:
                aboba.append(["Открыть резюме работника", "Удалить резюме работника"])
        except Exception:
            aboba.append("Создать резюме")
        try:
            if user_like_boss.phone:
                aboba.append(["Открыть резюме работодателя", "Удалить вакансию"])
        except Exception:
            aboba.append("Создать вакансию")
        for i in aboba:
            list_of_buttons.insert(1, i)
        keyboard = keyboard_creator(list_of_buttons)
        bot.send_message(message.from_user.id, f"Вы в главном меню", reply_markup=keyboard)
        return bot.register_next_step_handler(message, main_menu)
    elif message.text == "Очистить список вакансий":
        bot.send_message(message.from_user.id,
                         f"Эта функция в находится разработке. Выберите другой вариант в меню.")
        return bot.register_next_step_handler(message, main_menu)
    else:
        user_like_boss = session.query(Boss).filter(Boss.tg_id == message.from_user.id).first()
        user_like_people = session.query(People).filter(People.tg_id == message.from_user.id).first()
        list_of_buttons = [["Поиск работника", "Поиск работы"],
                           "Запись на обучение",
                           "Удалить всю информацию о себе"]
        try:
            if len(user_like_people.liked) > 0:
                list_of_buttons.insert(1, ["Посмотреть избранных работников", "Очистить список"])
        except Exception:
            pass
        try:
            if len(user_like_boss.liked) > 0:
                list_of_buttons.insert(1, ["Посмотреть избранные вакансии", "Очистить список"])
        except Exception:
            pass
        aboba = []
        try:
            if user_like_people.phone:
                aboba.append(["Мое резюме"])
        except Exception:
            aboba.append("Создать резюме работника")
        try:
            if user_like_boss.phone:
                aboba.append(["Мои вакансии"])
        except Exception:
            aboba.append("Создать вакансию")
        for i in aboba:
            list_of_buttons.insert(1, i)
        keyboard = keyboard_creator(list_of_buttons)
        bot.send_message(message.from_user.id, f"Вы в главном меню", reply_markup=keyboard)
        return bot.register_next_step_handler(message, main_menu)


@bot.callback_query_handler(
    func=lambda call: (call.data.split()[0].isdigit() and (
            (call.data.split()[1] in ["boss", "rab", "liked_boss"]) if " " in call.data else 0) or call.data in ['next',
                                                                                                                 'back',
                                                                                                                 "back_boss",
                                                                                                                 "next_boss",
                                                                                                                 "back_liked_boss",
                                                                                                                 "next_liked_boss",
                                                                                                                 "back_liked_rab",
                                                                                                                 "next_liked_rab"]))
def callback_worker(call):
    """
    это навигация в самом списке подходящих людей
    :param call: class; тг возвращает
    :return: ничего
    """
    if call.data == "back":
        text = call.message.text.split("\n")
        now_page = int(text[0].split()[1])
        if now_page - 1 >= 1:
            text[0] = f"Страница {now_page - 1} из {int(text[0].split()[3])}"
            key_dict = {"1": {"<": "back"}}
            for gg in range(1, 6):
                key_dict["1"][f"{(now_page - 2) * 5 + gg}"] = f"{(now_page - 2) * 5 + gg} rab"
            key_dict["1"][">"] = "next"
            list_poiska = search(call.message.chat.id)
            text = text[: 2]
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                text.append(
                    f"{(now_page - 2) * 5 + 1 + i}. {list_poiska[5 * (now_page - 2) + i].job}\n{int(list_poiska[5 * (now_page - 2) + i].salary)} р.")
            text = "\n".join(text)
        else:
            text[0] = f"Страница {int(text[0].split()[3])} из {int(text[0].split()[3])}"
            list_poiska = search(call.message.chat.id)
            key_dict = {"1": {"<": "back"}}
            now_page = int(text[0].split()[3]) - 1
            for i in range((len(list_poiska) - 1) % 5 + 1):
                key_dict["1"][f"{now_page * 5 + 1 + i}"] = f"{now_page * 5 + 1 + i} rab"
            key_dict["1"][">"] = "next"
            text = text[: 2]
            for i in range((len(list_poiska) - 1) % 5 + 1):
                text.append(
                    f"{now_page * 5 + 1 + i}. {list_poiska[5 * now_page + i].job}\n{int(list_poiska[5 * now_page + i].salary)} р.")
            text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "next":
        text = call.message.text.split("\n")
        list_poiska = search(call.message.chat.id)
        now_page = int(text[0].split()[1])
        if now_page + 1 <= int(text[0].split()[3]):
            if now_page + 1 != int(text[0].split()[3]):
                text[0] = f"Страница {now_page + 1} из {int(text[0].split()[3])}"
                key_dict = {"1": {"<": "back"}}
                for gg in range(1, 6):
                    key_dict["1"][f"{now_page * 5 + gg}"] = f"{now_page * 5 + gg} rab"
                key_dict["1"][">"] = "next"
                text = text[: 2]
                for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                    text.append(
                        f"{now_page * 5 + 1 + i}. {list_poiska[5 * now_page + i].job}\n{int(list_poiska[5 * now_page + i].salary)}  р.")
                text = "\n".join(text)
            else:
                text[0] = f"Страница {now_page + 1} из {int(text[0].split()[3])}"
                key_dict = {"1": {"<": "back"}}
                for i in range((len(list_poiska) - 1) % 5 + 1):
                    key_dict["1"][f"{now_page * 5 + i + 1}"] = f"{now_page * 5 + 1 + i} rab"
                key_dict["1"][">"] = "next"
                text = text[: 2]
                for i in range((len(list_poiska) - 1) % 5 + 1):
                    text.append(
                        f"{now_page * 5 + 1 + i}. {list_poiska[5 * now_page + i].job}\n{int(list_poiska[5 * now_page + i].salary)}  р.")
                text = "\n".join(text)
        else:
            text[0] = f"Страница 1 из {int(text[0].split()[3])}"
            key_dict = {"1": {"<": "back"}}
            for gg in range(1, 6):
                key_dict["1"][f"{gg}"] = f"{gg} rab"
            key_dict["1"][">"] = "next"
            text = text[: 2]
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                text.append(f"{1 + i}. {list_poiska[i].job}\n{int(list_poiska[i].salary)} р.")
            text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "back_boss":
        text = call.message.text.split("\n")
        now_page = int(text[0].split()[1])
        if now_page - 1 >= 1:
            text[0] = f"Страница {now_page - 1} из {int(text[0].split()[3])}"
            key_dict = {"1": {"<": "back_boss"}}
            for gg in range(1, 6):
                key_dict["1"][f"{(now_page - 2) * 5 + gg}"] = f"{(now_page - 2) * 5 + gg} boss"
            key_dict["1"][">"] = "next_boss"
            list_poiska = search_workers(call.message.chat.id)
            text = text[: 2]
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                text.append(
                    f"{(now_page - 2) * 5 + 1 + i}. {list_poiska[5 * (now_page - 2) + i].job}\n{int(list_poiska[5 * (now_page - 2) + i].salary)} р.")
            text = "\n".join(text)
        else:
            text[0] = f"Страница {int(text[0].split()[3])} из {int(text[0].split()[3])}"
            list_poiska = search_workers(call.message.chat.id)
            key_dict = {"1": {"<": "back_boss"}}
            now_page = int(text[0].split()[3]) - 1
            for i in range((len(list_poiska) - 1) % 5 + 1):
                key_dict["1"][f"{now_page * 5 + 1 + i}"] = f"{now_page * 5 + 1 + i} boss"
            key_dict["1"][">"] = "next_boss"
            text = text[: 2]
            for i in range((len(list_poiska) - 1) % 5 + 1):
                text.append(
                    f"{now_page * 5 + 1 + i}. {list_poiska[5 * now_page + i].job}\n{int(list_poiska[5 * now_page + i].salary)} р.")
            text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "next_boss":
        text = call.message.text.split("\n")
        list_poiska = search_workers(call.message.chat.id)
        now_page = int(text[0].split()[1])
        if now_page + 1 <= int(text[0].split()[3]):
            if now_page + 1 != int(text[0].split()[3]):
                text[0] = f"Страница {now_page + 1} из {int(text[0].split()[3])}"
                key_dict = {"1": {"<": "back_boss"}}
                for gg in range(1, 6):
                    key_dict["1"][f"{now_page * 5 + gg}"] = f"{now_page * 5 + gg} boss"
                key_dict["1"][">"] = "next_boss"
                text = text[: 2]
                for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                    text.append(
                        f"{now_page * 5 + 1 + i}. {list_poiska[5 * now_page + i].job}\n{int(list_poiska[5 * now_page + i].salary)}  р.")
                text = "\n".join(text)
            else:
                text[0] = f"Страница {now_page + 1} из {int(text[0].split()[3])}"
                key_dict = {"1": {"<": "back_boss"}}
                for i in range((len(list_poiska) - 1) % 5 + 1):
                    key_dict["1"][f"{now_page * 5 + i + 1}"] = f"{now_page * 5 + 1 + i} boss"
                key_dict["1"][">"] = "next_boss"
                text = text[: 2]
                for i in range((len(list_poiska) - 1) % 5 + 1):
                    text.append(
                        f"{now_page * 5 + 1 + i}. {list_poiska[5 * now_page + i].job}\n{int(list_poiska[5 * now_page + i].salary)}  р.")
                text = "\n".join(text)
        else:
            text[0] = f"Страница 1 из {int(text[0].split()[3])}"
            key_dict = {"1": {"<": "back_boss"}}
            for gg in range(1, 6):
                key_dict["1"][f"{gg}"] = f"{gg} boss"
            key_dict["1"][">"] = "next_boss"
            text = text[: 2]
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                text.append(f"{1 + i}. {list_poiska[i].job}\n{int(list_poiska[i].salary)} р.")
            text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "back_liked_boss":
        session = db_session.create_session()
        _list = liked(call.message.chat.id, 1)
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        nomer = int(user.count // 5 - 1 if user.count % 5 == 0 else user.count // 5)
        if nomer:
            text = []
            text.append(f"Страница 1 из {len(_list) // 5 if len(_list) % 5 == 0 else len(_list) // 5 + 1}")
            key_dict = {'1': {}}
            key_dict["1"]["<"] = "back_liked_boss"
            nomer -= 1
            _list = _list[nomer * 5: (nomer + 1) * 5]
            for gg in range(1, 6):
                key_dict["1"][f"{gg}"] = f"{gg} liked_boss"
            key_dict["1"][">"] = "next_liked_boss"
            text.append("")
            for i in range(5 if len(_list) >= 5 else len(_list) % 5):
                text.append(
                    f"{1 + i}. {_list[i].job}\n{int(_list[i].salary)} р.")
            text = "\n".join(text)
        else:
            pass
    elif call.data == "next_liked_boss":
        pass
    elif call.data.split()[1] == "boss" and call.data.split()[0].isdigit():
        session = db_session.create_session()
        text = call.message.text.split("\n")
        now_page = int(text[0].split()[1])
        text = []
        nomer = int(call.data.split()[0])
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        user_like_people = session.query(People).filter(People.tg_id == call.message.chat.id).first()
        _list = search_workers(tg_id=call.message.chat.id)
        chelik = session.query(Boss).filter(Boss.id == _list[nomer - 1].id).first()
        text.append(f"{chelik.name_of_vacancy}")
        text.append("")
        text.append(f"{int(chelik.salary)} руб.")
        text.append(f"{chelik.timetable}")
        text.append("")
        text.append(
            f"{chelik.trebovanija if len(chelik.trebovanija) <= 250 else f'{chelik.trebovanija[: 250]}(Подробнее в полном резюме)'}")
        dictt = {"1": {
            f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return_boss',
            'Контакты': 'cont_boss',
            'Полная версия': 'full_boss'
        }}
        try:
            if user_like_people.phone:
                dictt["2"] = {
                    f"{emojize(SMILE[3], use_aliases=True) if str(chelik.id) in user_like_people.liked else emojize(SMILE[2], use_aliases=True)}": f"like {chelik.id} boss"}
        except Exception:
            pass
        buttons = buttons_creator(dictt)
        text = "\n".join(text)
        user.count = int(call.data.split()[0])
        session.commit()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
    elif call.data.split()[1] == "rab" and call.data.split()[0].isdigit():
        session = db_session.create_session()
        text = call.message.text.split("\n")
        now_page = int(text[0].split()[1])
        text = []
        nomer = int(call.data.split()[0])
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        user_like_people = session.query(Boss).filter(Boss.tg_id == call.message.chat.id).first()
        _list = search(tg_id=call.message.chat.id)
        chelik = session.query(People).filter(People.id == _list[nomer - 1].id).first()
        text.append(f"{chelik.job}")
        text.append("")
        text.append(f"{int(chelik.salary)} руб.")
        text.append(f"{chelik.employment}")
        text.append("")
        text.append(
            f"{chelik.experience if len(chelik.experience) <= 250 else f'{chelik.experience[: 250]}(Подробнее в полном резюме)'}")
        dictt = {"1": {
            f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return',
            'Контакты': 'cont',
            'Полная версия': 'full'
        }}
        try:
            if user_like_people.phone:
                dictt["2"] = {
                    f"{emojize(SMILE[3], use_aliases=True) if str(chelik.id) in user_like_people.liked else emojize(SMILE[2], use_aliases=True)}": f"like {chelik.id} rab"}
        except Exception:
            pass
        buttons = buttons_creator(dictt)
        text = "\n".join(text)
        user.count = int(call.data.split()[0])
        session.commit()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
        # print(f"\033[0m{call.message.text}")
    elif call.data.split()[1] == "liked_boss" and call.data.split()[0].isdigit():
        session = db_session.create_session()
        text = []
        nomer = int(call.data.split()[0])
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        user_like_people = session.query(Boss).filter(Boss.tg_id == call.message.chat.id).first()
        _list = liked(tg_id=call.message.chat.id, who=1)
        chelik = session.query(People).filter(People.id == _list[nomer - 1].id).first()
        text.append(f"{chelik.job}")
        text.append("")
        text.append(f"{int(chelik.salary)} руб.")
        text.append(f"{chelik.employment}")
        text.append("")
        text.append(
            f"{chelik.experience if len(chelik.experience) <= 250 else f'{chelik.experience[: 250]}(Подробнее в полном резюме)'}")
        dictt = {"1": {
            f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return_liked_boss',
            'Контакты': 'cont_liked_boss',
            'Полная версия': 'full_liked_boss'
        }}
        try:
            if user_like_people.phone:
                dictt["2"] = {
                    f"{emojize(SMILE[3], use_aliases=True) if str(chelik.id) in user_like_people.liked else emojize(SMILE[2], use_aliases=True)}": f"like {chelik.id} rab_boss"}
        except Exception:
            pass
        buttons = buttons_creator(dictt)
        text = "\n".join(text)
        user.count = int(call.data.split()[0])
        session.commit()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)


@bot.callback_query_handler(
    func=lambda call: call.data in ['return', "return1", 'cont', 'full', "about", "about_boss", "return_boss",
                                    "cont_boss", "full_boss", "return_liked_boss", "cont_liked_boss",
                                    "full_liked_boss", "about_boss_liked"] or "like" == call.data.split()[0])
def callback2(call):
    """
    работа с определённым пользователем для списка
    :param call:
    :return:
    """
    print(call.data)
    if call.data == 'return':
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        list_poiska = search(call.message.chat.id)
        key_dict = {"1": {}}
        if len(list_poiska) > 5:
            key_dict["1"]["<"] = "back"
        text = call.message.text.split("\n")
        nomer = user.count
        text = [
            f"Страница {nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1} из {len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1}",
            ""]
        for i in range((5 if (len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1) != (
                nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1) else len(list_poiska) % 5) if len(
            list_poiska) != 5 else 5):
            nomer1 = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            string = f"{1 + i}. {list_poiska[nomer1 * 5 + i].job}\n{int(list_poiska[nomer1 * 5 + i].salary)} р."
            text.append(string)
        text = "\n".join(text)
        for i in range((5 if (len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1) != (
                nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1) else len(list_poiska) % 5) if len(
            list_poiska) != 5 else 5):
            hz = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            key_dict["1"][f"{hz * 5 + i + 1}"] = f"{hz * 5 + i + 1} rab"
        if len(list_poiska) > 5:
            key_dict["1"][">"] = "next"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == 'return1':
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        list_poiska = search(call.message.chat.id)
        key_dict = {"1": {"<": "back"}}
        nomer = user.count
        text = [
            f"Страница {nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1} из {len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1}",
            ""]
        for i in range(5 if (len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1) != (
                nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1) else len(list_poiska) % 5):
            nomer1 = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            string = f"{1 + i}. {list_poiska[nomer1 * 5 + i].job}\n{int(list_poiska[nomer1 * 5 + i].salary)} р."
            text.append(string)
        text = "\n".join(text)
        for i in range(5 if (len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1) != (
                nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1) else len(list_poiska) % 5):
            hz = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            key_dict["1"][f"{hz * 5 + i + 1}"] = f"{hz * 5 + i + 1}"
        key_dict["1"][">"] = "next"
        bot.send_message(call.message.chat.id, text, reply_markup=buttons_creator(key_dict))
    elif call.data == "about":
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        text = call.message.text.split("\n")
        text = []
        nomer = user.count
        _list = search(call.message.chat.id)
        chelik = session.query(People).filter(People.id == _list[nomer - 1].id).first()
        text.append(f"{chelik.job}")
        text.append("")
        text.append(f"{chelik.salary}")
        text.append(f"{chelik.employment}")
        text.append("")
        text.append(
            f"{chelik.experience if len(chelik.experience) <= 250 else f'{chelik.experience[: 250]}(Подробнее в полном резюме)'}")
        buttons = buttons_creator({"1": {
            f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return',
            'Контакты': 'cont',
            'Полная версия': 'full'
        }})
        text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
    elif call.data == 'cont':
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        data = Data()
        text = call.message.text.split("\n")
        text = []
        nomer = user.count
        text.append("Вот контактная информация:")
        text.append("")
        _list = search(call.message.chat.id)
        chelik = session.query(People).filter(People.id == _list[nomer - 1].id).first()
        text.append(f"{chelik.name}")
        text.append(f"{chelik.phone}")
        text.append(f"{chelik.mail}")
        text = "\n".join(text)
        data.tg_id_boss = call.message.message_id
        data.arg1 = user.arg1
        data.arg2 = user.arg2
        data.arg3 = user.arg3
        data.tg_id_people = chelik.id
        session.add(data)
        session.commit()
        buttons = buttons_creator({'1': {f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'about'}})
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
    elif call.data == 'full':
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        nomer = user.count
        _list = search(call.message.chat.id)
        chelik = session.query(People).filter(People.id == _list[nomer - 1].id).first()
        pdf(chelik.id)
        data = Data()
        data.tg_id_boss = call.message.message_id
        data.arg1 = user.arg1
        data.arg2 = user.arg2
        data.arg3 = user.arg3
        data.tg_id_people = chelik.id
        session.add(data)
        session.commit()
        buttons = buttons_creator({'1': {f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return1'}})
        bot.send_document(call.message.chat.id, open("data/media/resume.pdf", 'rb'), reply_markup=buttons)
    elif call.data == "cont_boss":
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        data = Data()
        text = call.message.text.split("\n")
        text = []
        nomer = user.count
        text.append("Вот контактная информация:")
        text.append("")
        _list = search_workers(call.message.chat.id)
        chelik = session.query(Boss).filter(Boss.id == _list[nomer - 1].id).first()
        text.append(f"{chelik.name_of_rab}")
        text.append(f"{chelik.phone}")
        text.append(f"{chelik.email}")
        text = "\n".join(text)
        data.tg_id_boss = call.message.message_id
        data.arg1 = user.arg1
        data.arg2 = user.arg2
        data.arg3 = user.arg3
        data.tg_id_people = chelik.id
        session.add(data)
        session.commit()
        buttons = buttons_creator({'1': {f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'about_boss'}})
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
    elif call.data == "cont_liked_boss":
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        data = Data()
        text = call.message.text.split("\n")
        text = []
        nomer = user.count
        text.append("Вот контактная информация:")
        text.append("")
        _list = liked(call.message.chat.id, 1)
        chelik = session.query(People).filter(People.id == _list[nomer - 1].id).first()
        text.append(f"{chelik.name}")
        text.append(f"{chelik.phone}")
        text.append(f"{chelik.mail}")
        text = "\n".join(text)
        data.tg_id_boss = call.message.message_id
        data.arg1 = user.arg1
        data.arg2 = user.arg2
        data.arg3 = user.arg3
        data.tg_id_people = chelik.id
        session.add(data)
        session.commit()
        buttons = buttons_creator({'1': {f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'about_boss_liked'}})
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
    elif call.data == "full_boss":
        pass
    elif call.data == "return_liked_boss":
        session = db_session.create_session()
        text = []
        user_like_boss = session.query(Boss).filter(Boss.tg_id == call.message.chat.id).first()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        if len(user_like_boss.liked) > 0:
            _list = liked(call.message.chat.id, 1)
            text.append(
                f"Страница {user.count // 5 if user.count % 5 == 0 else user.count // 5 + 1} из {len(_list) // 5 if len(_list) % 5 == 0 else len(_list) // 5 + 1}")
            key_dict = {'1': {}}
            if len(_list) > 5:
                key_dict["1"]["<"] = "back_liked_boss"
            for gg in range(1, len(_list) + 1):
                key_dict["1"][
                    f"{(user.count // 5 - 1 if user.count % 5 == 0 else user.count // 5) * 5 + gg}"] = f"{(user.count // 5 - 1 if user.count % 5 == 0 else user.count // 5) * 5 + gg} liked_boss"
            if len(_list) > 5:
                key_dict["1"][">"] = "next_liked_boss"
            text.append("")
            for i in range(5 if len(_list) >= 5 else len(_list) % 5):
                text.append(f"{1 + i}. {_list[i].job}\n{int(_list[i].salary)} р.")
            text = "\n".join(text)
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                  reply_markup=buttons_creator(key_dict))
        else:
            user_like_boss = session.query(Boss).filter(Boss.tg_id == call.message.message_id).first()
            user_like_people = session.query(People).filter(People.tg_id == call.message.message_id).first()
            list_of_buttons = [["Поиск работника", "Поиск работы"],
                               "Запись на обучение",
                               "Удалить всю информацию о себе"]
            try:
                if len(user_like_people.liked) > 0:
                    list_of_buttons.insert(1, ["Посмотреть избранных работников", "Очистить список"])
            except Exception:
                pass
            try:
                if len(user_like_boss.liked) > 0:
                    list_of_buttons.insert(1, ["Посмотреть избранные вакансии", "Очистить список"])
            except Exception:
                pass
            aboba = []
            try:
                if user_like_people.phone:
                    aboba.append(["Мое резюме"])
            except Exception:
                aboba.append("Создать резюме")
            try:
                if user_like_boss.phone:
                    aboba.append(["Мои вакансии"])
            except Exception:
                aboba.append("Создать вакансию")
            for i in aboba:
                list_of_buttons.insert(1, i)
            keyboard = keyboard_creator(list_of_buttons)
            bot.send_message(call.message.chat.id, "Вы в главном меню", reply_markup=keyboard)
    elif call.data == "return_boss":
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        list_poiska = search_workers(call.message.chat.id)
        key_dict = {"1": {}}
        if len(list_poiska) > 5:
            key_dict["1"]["<"] = "back_boss"
        text = call.message.text.split("\n")
        nomer = user.count
        text = [
            f"Страница {nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1} из {len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1}",
            ""]
        for i in range((5 if (len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1) != (
                nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1) else len(list_poiska) % 5) if len(
            list_poiska) != 5 else 5):
            nomer1 = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            string = f"{1 + i}. {list_poiska[nomer1 * 5 + i].job}\n{int(list_poiska[nomer1 * 5 + i].salary)} р."
            text.append(string)
        text = "\n".join(text)
        for i in range((5 if (len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1) != (
                nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1) else len(list_poiska) % 5) if len(
            list_poiska) != 5 else 5):
            hz = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            key_dict["1"][f"{hz * 5 + i + 1}"] = f"{hz * 5 + i + 1} boss"
        if len(list_poiska) > 5:
            key_dict["1"][">"] = "next_boss"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "about_boss":
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        text = call.message.text.split("\n")
        text = []
        nomer = user.count
        _list = search_workers(call.message.chat.id)
        chelik = session.query(Boss).filter(Boss.id == _list[nomer - 1].id).first()
        user_like_people = session.query(Boss).filter(Boss.tg_id == call.message.chat.id).first()
        text.append(f"{chelik.name_of_vacancy}")
        text.append("")
        text.append(f"{chelik.salary}")
        text.append(f"{chelik.timetable}")
        text.append("")
        text.append(
            f"{chelik.trebovanija if len(chelik.trebovanija) <= 250 else f'{chelik.trebovanija[: 250]}(Подробнее в полной версии вакансии)'}")
        dictt = {"1": {
            f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return_boss',
            'Контакты': 'cont_boss',
            'Полная версия': 'full_boss'
        }}
        try:
            if user_like_people.phone:
                dictt["2"] = {
                    f"{emojize(SMILE[3], use_aliases=True) if str(chelik.id) in user_like_people.liked else emojize(SMILE[2], use_aliases=True)}": f"like {chelik.id} boss"}
        except Exception:
            pass
        buttons = buttons_creator(dictt)
        text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
    elif call.data == "about_boss_liked":
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        text = []
        nomer = user.count
        _list = liked(call.message.chat.id, 1)
        chelik = session.query(People).filter(People.id == _list[nomer - 1].id).first()
        user_like_people = session.query(Boss).filter(Boss.tg_id == call.message.chat.id).first()
        text.append(f"{chelik.job}")
        text.append("")
        text.append(f"{int(chelik.salary)}")
        text.append(f"{chelik.employment}")
        text.append("")
        text.append(
            f"{chelik.experience if len(chelik.experience) <= 250 else f'{chelik.experience[: 250]}(Подробнее в полном резюме)'}")
        dictt = {"1": {
            f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return_liked_boss',
            'Контакты': 'cont_liked_boss',
            'Полная версия': 'full_liked_boss'
        }}
        try:
            if user_like_people.phone:
                dictt["2"] = {
                    f"{emojize(SMILE[3], use_aliases=True) if str(chelik.id) in user_like_people.liked else emojize(SMILE[2], use_aliases=True)}": f"like {chelik.id} rab_boss"}
        except Exception:
            pass
        buttons = buttons_creator(dictt)
        text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
    elif "like" == call.data.split()[0] and "boss" == call.data.split()[2]:
        session = db_session.create_session()
        user = session.query(People).filter(People.tg_id == call.message.chat.id).first()
        if call.data.split()[1] in user.liked:
            _list = user.liked.split(',')
            new_list = []
            for i in _list:
                if i.isdigit():
                    new_list.append(i)
            _list = new_list
            _list.pop(_list.index(call.data.split()[1]))
            user.liked = ",".join(_list)
            session.commit()
            text = call.message.text
            buttons = buttons_creator({"1": {
                f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return',
                'Контакты': 'cont',
                'Полная версия': 'full'
            },
                "2": {
                    f"{emojize(SMILE[2], use_aliases=True)}": f"like {call.data.split()[1]}"}
            })
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                  reply_markup=buttons)
        else:
            aboba = user.liked.split(",")
            new_list = []
            for i in aboba:
                if i.isdigit():
                    new_list.append(i)
            aboba = new_list
            aboba.append(call.data.split()[1])
            user.liked = ",".join(aboba)
            session.commit()
            text = call.message.text
            buttons = buttons_creator({"1": {
                f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return',
                'Контакты': 'cont',
                'Полная версия': 'full'
            },
                "2": {
                    f"{emojize(SMILE[3], use_aliases=True)}": f"like {call.data.split()[1]}"}
            })
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                  reply_markup=buttons)
    elif "like" == call.data.split()[0] and "rab" == call.data.split()[2]:
        session = db_session.create_session()
        user = session.query(Boss).filter(Boss.tg_id == call.message.chat.id).first()
        if call.data.split()[1] in user.liked:
            _list = user.liked.split(',')
            new_list = []
            for i in _list:
                if i.isdigit():
                    new_list.append(i)
            _list = new_list
            _list.pop(_list.index(call.data.split()[1]))
            user.liked = ",".join(_list)
            session.commit()
            text = call.message.text
            buttons = buttons_creator({"1": {
                f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return',
                'Контакты': 'cont',
                'Полная версия': 'full'
            },
                "2": {
                    f"{emojize(SMILE[2], use_aliases=True)}": f"like {call.data.split()[1]}"}
            })
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                  reply_markup=buttons)
        else:
            aboba = user.liked.split(",")
            new_list = []
            for i in aboba:
                if i.isdigit():
                    new_list.append(i)
            aboba = new_list
            aboba.append(call.data.split()[1])
            user.liked = ",".join(aboba)
            session.commit()
            text = call.message.text
            buttons = buttons_creator({"1": {
                f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return',
                'Контакты': 'cont',
                'Полная версия': 'full'
            },
                "2": {
                    f"{emojize(SMILE[3], use_aliases=True)}": f"like {call.data.split()[1]}"}
            })
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                  reply_markup=buttons)
    elif "like" == call.data.split()[0] and "rab_boss" == call.data.split()[2]:
        session = db_session.create_session()
        user = session.query(Boss).filter(Boss.tg_id == call.message.chat.id).first()
        if call.data.split()[1] in user.liked:
            _list = user.liked.split(',')
            new_list = []
            for i in _list:
                if i.isdigit():
                    new_list.append(i)
            _list = new_list
            _list.pop(_list.index(call.data.split()[1]))
            user.liked = ",".join(_list)
            session.commit()
            text = call.message.text
            buttons = buttons_creator({"1": {
                f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return_liked_boss',
                'Контакты': 'cont_liked_boss',
                'Полная версия': 'full_liked_boss'
            },
                "2": {
                    f"{emojize(SMILE[2], use_aliases=True)}": f"like {call.data.split()[1]} rab_boss"}
            })
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                  reply_markup=buttons)
        else:
            aboba = user.liked.split(",")
            new_list = []
            for i in aboba:
                if i.isdigit():
                    new_list.append(i)
            aboba = new_list
            aboba.append(call.data.split()[1])
            user.liked = ",".join(aboba)
            session.commit()
            text = call.message.text
            buttons = buttons_creator({"1": {
                f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return_liked_boss',
                'Контакты': 'cont_liked_boss',
                'Полная версия': 'full_liked_boss'
            },
                "2": {
                    f"{emojize(SMILE[3], use_aliases=True)}": f"like {call.data.split()[1]} rab_boss"}
            })
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                  reply_markup=buttons)


for _ in range(10):
    try:
        print('\033[0mStarted.....')
        log()
        # bot.polling(none_stop=True)
        bot.infinity_polling()
    except Exception as err:
        print('\033[31mCrashed.....')
        print(f"Error: {err}")
        time.sleep(10)
        print('\033[35mRestarting.....')

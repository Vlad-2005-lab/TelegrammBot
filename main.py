# -*- coding: utf-8 -*-

# import random
import telebot
import pdfcrowd
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
bot = telebot.TeleBot(open('data/media/token.txt').read())
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
                    part_1.append(Human(id=i.id, job=i.name_vacancy, salary=i.salary, r=r))
                elif p >= 0.5:
                    part_2.append(Human(id=i.id, job=i.name_vacancy, salary=i.salary, r=r))
                elif p >= 0.25:
                    part_3.append(Human(id=i.id, job=i.name_vacancy, salary=i.salary, r=r))
                elif p >= 0:
                    part_4.append(Human(id=i.id, job=i.name_vacancy, salary=i.salary, r=r))
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
    client = pdfcrowd.HtmlToPdfClient("AVI2005", "5ec73c962bac1db58b3e27d9dd183a86")
    client.setPageWidth("1400px")
    client.setPageHeight("2000px")
    client.convertFileToFile("data/media/pdf.html", 'data/media/resume.pdf')


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
                                 "Оставить резюме работодателя", "Оставить резюме работника",
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
                aboba.append(["Резюме работника", "Удалить резюме работника"])
        except Exception:
            aboba.append("Создать резюме работника")
        try:
            if user_like_boss.phone:
                aboba.append(["Резюме работодателя", "Удалить резюме работодателя"])
        except Exception:
            aboba.append("Создать резюме работодателя")
        for i in aboba:
            list_of_buttons.insert(1, i)
        keyboard = keyboard_creator(list_of_buttons)
        bot.send_message(message.from_user.id, f"Вы в глваном меню", reply_markup=keyboard)
        return bot.register_next_step_handler(message, main_menu)
    bot.send_message(message.from_user.id, f"Здраствуйте")
    bot.send_message(message.from_user.id, f"Что вас интересует?", reply_markup=keyboard)
    return bot.register_next_step_handler(message, vilka)


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
        elif message.text == "Оставить резюме работодателя":
            bot.send_message(message.from_user.id,
                             f"Введите своё имя.",
                             reply_markup=keyboard)
            return bot.register_next_step_handler(message, start_creating_vacancy)
        elif message.text == "Оставить резюме работника":
            bot.send_message(message.from_user.id,
                             f"Введите своё имя.",
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
            bos.fio = message.text
            bos.tg_id = message.from_user.id
            bos.count = 1
            session.add(bos)
            session.commit()
            bot.send_message(message.from_user.id, f"Введите номер телефона.", reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_vacancy)
    except Exception as er:
        print(er)


def start_creating_tender(message):
    pass


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
            phone = ""
            for i in message.text:
                if i.isdigit():
                    phone += i
            if len(phone) == 11:
                user.phone = phone
                user.count += 1
                session.commit()
                bot.send_message(message.from_user.id, f"Введите свой email.", reply_markup=types.ReplyKeyboardRemove())
                return bot.register_next_step_handler(message, creating_vacancy)
            else:
                bot.send_message(message.from_user.id, f"Вы ввели не правильный номер телефона.", reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 2:
            email = message.text.replace(" ", "")
            if correctemail(email):
                user.email = email
                user.count += 1
                session.commit()
                bot.send_message(message.from_user.id, f"Введите город в котором вы живете.",
                                 reply_markup=types.ReplyKeyboardRemove())
                return bot.register_next_step_handler(message, creating_vacancy)
            else:
                bot.send_message(message.from_user.id, f"Вы ввели не правильный email.", reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 3:
            user.city = str(message.text)
            user.count += 1
            session.commit()
            bot.send_message(message.from_user.id, f"Введите название должности/ей, основной стек через пробелы",
                             reply_markup=types.ReplyKeyboardRemove())
            return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 4:
            user.count += 1
            session.commit()
            list_of_jobs = str(message.text).replace(";", " ").replace("/", " ").replace(
                "|", " ").replace("~", " ").replace(":", " ").replace("{", " ").replace("}", " ").replace("[",
                                                                                                          " ").replace(
                "]", " ").replace("+", " ").replace("-", " ")
            # nekotorie mohinacii c vvodom
            user.name_vacancy = ", ".join(list_of_jobs.split())
            session.commit()
            bot.send_message(message.from_user.id, f"Напишите свои требования к работнику/ам.",
                             reply_markup=types.ReplyKeyboardRemove())
            return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 5:
            user.count += 1
            user.trebovanija = message.text
            session.commit()
            text = user.name_vacancy + " " + user.trebovanija
            shit = ""
            for sign in text:
                if sign.isalpha() or sign.isdigit() or sign == " ":
                    shit += sign
            text = shit
            tags = []
            for word in text.split():
                skip = False
                for keys in SINONIMS.keys():
                    if word in list(SINONIMS[keys]):
                        tags.append(keys)
                        skip = True
                        break
                if skip:
                    continue
                if word in jobs:
                    tags.append(word)
                    continue
            tags = list(set(tags))
            user.tags = " ".join(tags)
            session.commit()
            bot.send_message(message.from_user.id, f"Какую ЗП вы хотели бы платить работнику/ам?")
            return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 6:
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
            bot.send_message(message.from_user.id, f"Какую занятость вы предлогаете?",
                             reply_markup=keyboard)
            return bot.register_next_step_handler(message, creating_vacancy)
        elif user.count == 7:
            if message.text in ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость",
                                "Все варианты"]:
                user.count = 0
                user.timetable = message.text
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
                        aboba.append(["Резюме работника", "Удалить резюме работника"])
                except Exception:
                    aboba.append("Создать резюме работника")
                try:
                    if user_like_boss.phone:
                        aboba.append(["Резюме работодателя", "Удалить резюме работодателя"])
                except Exception:
                    aboba.append("Создать резюме работодателя")
                for i in aboba:
                    list_of_buttons.insert(1, i)
                keyboard = keyboard_creator(list_of_buttons)
                bot.send_message(message.from_user.id, f"Вы в главном меню", reply_markup=keyboard)
                return bot.register_next_step_handler(message, main_menu)
            else:
                keyboard = keyboard_creator(
                    ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость", "Все варианты",
                     f"{emojize(SMILE[1], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"К сожалению нет такого варианта, попробуйте другой вариант.",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, creating_vacancy)
    except Exception as er:
        print(er)


def creating_tender(message):
    pass


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
    elif message.text == "Удалить резюме работника":
        user_like_people = session.query(People).filter(People.tg_id == message.from_user.id).first()
        session.delete(user_like_people)
        session.commit()
        return have_vacancy(message)
    elif message.text == "Удалить резюме работодателя":
        user_like_boss = session.query(Boss).filter(Boss.tg_id == message.from_user.id).first()
        session.delete(user_like_boss)
        session.commit()
        return have_vacancy(message)
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
                aboba.append(["Открыть резюме работника", "Удалить резюме работника"])
        except Exception:
            aboba.append("Создать резюме работника")
        try:
            if user_like_boss.phone:
                aboba.append(["Открыть резюме работодателя", "Удалить резюме работодателя"])
        except Exception:
            aboba.append("Создать резюме работодателя")
        for i in aboba:
            list_of_buttons.insert(1, i)
        keyboard = keyboard_creator(list_of_buttons)
        bot.send_message(message.from_user.id, f"Вы в глваном меню", reply_markup=keyboard)
        return bot.register_next_step_handler(message, main_menu)


@bot.callback_query_handler(
    func=lambda call: (call.data.split()[0].isdigit() and ((call.data.split()[1] in ["boss", "rab"]) if " " in call.data else 0) or call.data in ['next', 'back', "back_boss", "next_boss"]))
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
                key_dict["1"][f"{(now_page - 2) * 5 + gg}"] = f"{(now_page - 2) * 5 + gg}"
            key_dict["1"][">"] = "next"
            list_poiska = search(call.message.chat.id)
            text = text[: 2]
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                text.append(
                    f"{1 + i}. {list_poiska[5 * (now_page - 2) + i].job}\n{int(list_poiska[5 * (now_page - 2) + i].salary)} р.")
            text = "\n".join(text)
        else:
            text[0] = f"Страница {int(text[0].split()[3])} из {int(text[0].split()[3])}"
            list_poiska = search(call.message.chat.id)
            key_dict = {"1": {"<": "back"}}
            now_page = int(text[0].split()[3]) - 1
            for i in range((len(list_poiska) - 1) % 5 + 1):
                key_dict["1"][f"{now_page * 5 + 1 + i}"] = f"{now_page * 5 + 1 + i}"
            key_dict["1"][">"] = "next"
            text = text[: 2]
            for i in range((len(list_poiska) - 1) % 5 + 1):
                text.append(
                    f"{1 + i}. {list_poiska[5 * now_page + i].job}\n{int(list_poiska[5 * now_page + i].salary)} р.")
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
                    key_dict["1"][f"{now_page * 5 + gg}"] = f"{now_page * 5 + gg}"
                key_dict["1"][">"] = "next"
                text = text[: 2]
                for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                    text.append(
                        f"{1 + i}. {list_poiska[5 * now_page + i].job}\n{int(list_poiska[5 * now_page + i].salary)}  р.")
                text = "\n".join(text)
            else:
                text[0] = f"Страница {now_page + 1} из {int(text[0].split()[3])}"
                key_dict = {"1": {"<": "back"}}
                for i in range((len(list_poiska) - 1) % 5 + 1):
                    key_dict["1"][f"{now_page * 5 + i + 1}"] = f"{now_page * 5 + 1 + i}"
                key_dict["1"][">"] = "next"
                text = text[: 2]
                for i in range((len(list_poiska) - 1) % 5 + 1):
                    text.append(
                        f"{1 + i}. {list_poiska[5 * now_page + i].job}\n{int(list_poiska[5 * now_page + i].salary)}  р.")
                text = "\n".join(text)
        else:
            text[0] = f"Страница 1 из {int(text[0].split()[3])}"
            key_dict = {"1": {"<": "back"}}
            for gg in range(1, 6):
                key_dict["1"][f"{gg}"] = f"{gg}"
            key_dict["1"][">"] = "next"
            text = text[: 2]
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                text.append(f"{1 + i}. {list_poiska[i].job}\n{int(list_poiska[i].salary)} р.")
            text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "back_boss":
        print(call.data)
    elif call.data == "next_boss":
        print(call.data)
    elif call.data.split()[1] == "boss" and call.data.split()[0].isdigit():
        print(call.data)
    else:
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
            'Полное резюме': 'full'
        }}
        try:
            if user_like_people.phone:
                dictt["2"] = {
                    f"{emojize(SMILE[3], use_aliases=True) if str(chelik.id) in user_like_people.liked else emojize(SMILE[2], use_aliases=True)}": f"like {chelik.id}"}
        except Exception:
            pass
        buttons = buttons_creator(dictt)
        text = "\n".join(text)
        user.count = int(call.data.split()[0])
        session.commit()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
        # print(f"\033[0m{call.message.text}")


@bot.callback_query_handler(
    func=lambda call: call.data in ['return', "return1", 'cont', 'full', "about"] or "like" in call.data)
def callback2(call):
    """
    работа с определённым пользователем для списка
    :param call:
    :return:
    """
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
            'Полное резюме': 'full'
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
    elif "like" in call.data:
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
                'Полное резюме': 'full'
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
                'Полное резюме': 'full'
            },
                "2": {
                    f"{emojize(SMILE[3], use_aliases=True)}": f"like {call.data.split()[1]}"}
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

# -*- coding: utf-8 -*-import random

import random
import telebot
from emoji import emojize
from telebot import types
from data.banned import Ban
from data.people import People
# from data.boss import Boss
from data import db_session
import time
import datetime
import re

SMILE = ['↩']
bot = telebot.TeleBot('1625541968:AAF0Hrv_57dx8x1osP56CxnxSejWu-kWijc')
print('\033[35mStarting.....')
count = -1
history = True
print('\033[35mConnecting to db....')
db_session.global_init("db/resume.sqlite")
print('\033[35mDb was conected...')


def tconv(x):
    return time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))


def log(message=None, where='ne napisal', full=False, comments="None"):
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


def keyboard_creator(list_of_names):
    returned_k = telebot.types.ReplyKeyboardMarkup()
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


def buttons_creator(dict_of_names, how_many_rows=7):
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
    session = db_session.create_session()
    user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
    user.time = tconv(message.date)
    session.commit()


class Chelik:
    def __init__(self, **args):
        for i in args.keys():
            if type(args[i]) is str:
                exec(f"self.{i} = '{args[i]}'")
            else:
                exec(f"self.{i} = {args[i]}")


def machinazii_s_poiskom(tg_id=-1):
    try:
        if tg_id == -1:
            # adekvatnaja hren, no ne sejchas
            list_of_dodik = []
            session = db_session.create_session()
            users = session.query(People).all()
            for i in users:
                list_of_dodik.append(Chelik(id=i.id, job=i.job, salary=i.salary))
            return list_of_dodik
    except Exception as ex:
        log(full=True, where="machinazii_s_poiskom", comments=str(ex))


#
# def loginned(message):
#     id = message.from_user.id
#     session = db_session.create_session()
#     try:
#         object1 = session.query(People).filter(People.tg_id == id).first()
#         if object1.who != "none":
#             if not object1.pozizninij_ban:
#                 pass
#             else:
#                 return "etot kretin zabanen"
#         else:
#             if object1.count == 0:
#                 session.delete(object1)
#                 session.commit()
#             message.text = "Искать работу"
#             return ["r", message]
#         return True
#     except Exception:
#         object2 = session.query(Boss).filter(Boss.tg_id == id).first()
#         try:
#             if object2.sity != "none":
#                 if not object2.pozizninij_ban:
#                     pass
#                 else:
#                     return "etot kretin zabanen"
#             else:
#                 if object2.count == 0:
#                     session.delete(object2)
#                     session.commit()
#                 message.text = "Искать людей"
#                 return ["r", message]
#             return True
#         except Exception:
#             return False
#
#
# def who(id):
#     s = db_session.create_session()
#     try:
#         man = s.query(People).filter(People.tg_id == id).first()
#         assert len(man.about) > 0
#         return 'people'
#     except Exception as er:
#         return 'boss'

# @bot.message_handler(commands=['start'])
# def help_function(message):
#     print("\033[0mdadadada")
#
#
#
# @bot.message_handler(commands=['help'])
# def help_function(message):
#     print("help")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
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
            session.add(user)
            session.commit()
        update(message)
        log(message=message, where="get_text_messages")
        # answer = loginned(message)
        # try:
        #     if answer[0] == "r":
        #         return bot.register_next_step_handler(answer[1], register)
        #     try:
        #         answer = bool(answer)
        #     except Exception:
        #         bot.send_message(message.from_user.id,
        #                          f"Ты забанен, теряйся клоун")
        #         return 0
        # except Exception:
        #     pass
        # if not answer:
        #     if message.text in ["Привет", "/start", 'Здравствуйте']:
        #         keyboard = keyboard_creator([["Хорошо",
        #                                       "Нет"]])
        #         bot.send_message(message.from_user.id,
        #                          f"Добрый день {message.from_user.username if message.from_user.username else str(message.from_user.last_name) + ' ' + message.from_user.first_name}, предлагаю вам указать свои данные",
        #                          reply_markup=keyboard)
        #     elif message.text in ["Указать информацию", "Хорошо"]:
        #         keyboard = keyboard_creator(['Искать работу', 'Искать людей'])
        #         bot.send_message(message.from_user.id,
        #                          f"Добро пожаловать в раздел регистрации, ответы пишите в одном сообщении. Если что-то пойдёт не так, вы сможете перезаполнить о себе данные")
        #         bot.send_message(message.from_user.id,
        #                          f"Вы хотите нанять на работу людей или нанятся на работу?",
        #                          reply_markup=keyboard)
        #         return bot.register_next_step_handler(message, register)
        #     elif message.text == "Нет":
        #         bot.send_message(message.from_user.id, "Напишите, когда передумаете")
        #     else:
        #         keyboard = keyboard_creator([["Здравствуйте",
        #                                       "Привет"],
        #                                      "Указать информацию"])
        #         bot.send_message(message.from_user.id,
        #                          "Извините, я вас не понимаю.\nПредагаю вам написать:\nПривет\nЗдравствуйте\nУказать информацию",
        #                          reply_markup=keyboard)
        # else:
        #     bot.send_message(message.from_user.id,
        #                      f"Добрый день {message.from_user.username if message.from_user.username else message.from_user.last_name + ' ' + message.from_user.first_name}")
        #     return bot.register_next_step_handler(message, main_menu)
        keyboard = keyboard_creator([["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
                                     "Расписание обучения"])
        # bot.send_message(message.from_user.id, f"Здраствуйте {emojize('⬆', use_aliases=True)}")
        bot.send_message(message.from_user.id, f"Здраствуйте")
        bot.send_message(message.from_user.id, f"Что вас интересует?", reply_markup=keyboard)
        return bot.register_next_step_handler(message, vilka)
    except Exception as er:
        log(message=message, where="get_text_messages", comments=str(er))


def vilka(message):
    try:
        log(message=message, where="vilka")
        keyboard = keyboard_creator([f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню"])
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
            user.time = tconv(message.date)
            session.add(user)
            session.commit()
        update(message)
        if message.text == "Поиск работника":
            bot.send_message(message.from_user.id,
                             f"Какая у вас вакансия? Введите название должности, основной стек через пробелы",
                             reply_markup=keyboard)
            return bot.register_next_step_handler(message, porashnaja_funkcia_dla_poiska_rabotnikov_1)
        elif message.text == "Поиск работы":
            bot.send_message(message.from_user.id,
                             f"Эта функция в находится разработке. Выберите другой вариант в меню.")
            return bot.register_next_step_handler(message, vilka)
        elif message.text == "Оставить резюме":
            bot.send_message(message.from_user.id,
                             f"Эта функция в находится разработке. Выберите другой вариант в меню.")
            return bot.register_next_step_handler(message, vilka)
        elif message.text == "Запись на обучение":
            bot.send_message(message.from_user.id,
                             f"Эта функция в находится разработке. Выберите другой вариант в меню.")
            return bot.register_next_step_handler(message, vilka)
        elif message.text == "Расписание обучения":
            bot.send_message(message.from_user.id,
                             f"Эта функция в находится разработке. Выберите другой вариант в меню.")
            return bot.register_next_step_handler(message, vilka)
        else:
            bot.send_message(message.from_user.id, f"Извините, но такого варианта нет.")
            return bot.register_next_step_handler(message, vilka)
    except Exception as er:
        log(message=message, full=True, where="vilka", comments=str(er))


def porashnaja_funkcia_dla_poiska_rabotnikov_1(message):
    try:
        log(message=message, where="porashnaja_funkcia_dla_poiska_rabotnikov_1")
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
            user.time = tconv(message.date)
            session.add(user)
            session.commit()
            session.close()
        update(message)
        keyboard = keyboard_creator([["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
                                     "Расписание обучения"])
        if message.text == f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню":
            keyboard = keyboard_creator([["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
                                         "Расписание обучения"])
            bot.send_message(message.from_user.id, f"Что вас интересует?", reply_markup=keyboard)
            return bot.register_next_step_handler(message, vilka)
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
                 f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню"])
            bot.send_message(message.from_user.id, f"Что вы предлагаете?", reply_markup=keyboard)
            return bot.register_next_step_handler(message,
                                                  porashnaja_funkcia_dla_poiska_rabotnikov_2)
    except Exception as er:
        log(message=message, full=True, where="porashnaja_funkcia_dla_poiska_rabotnikov_1", comments=str(er))


def porashnaja_funkcia_dla_poiska_rabotnikov_2(message):
    try:
        log(message=message, where="porashnaja_funkcia_dla_poiska_rabotnikov_2")
        keyboard = keyboard_creator(
            ["Стажировка", "Проектная работа", "Частичная занятость", "Полная занятость", "Все варианты",
             f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню"])
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
            user.time = tconv(message.date)
            session.add(user)
            session.commit()
            session.close()
        update(message)
        if message.text == f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню":
            keyboard = keyboard_creator([["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
                                         "Расписание обучения"])
            bot.send_message(message.from_user.id, f"Что вас интересует?", reply_markup=keyboard)
            return bot.register_next_step_handler(message, vilka)
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
                return bot.register_next_step_handler(message, porashnaja_funkcia_dla_poiska_rabotnikov_2)
            keyboard = keyboard_creator([f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню"])
            session = db_session.create_session()
            user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
            user.arg2 = message.text
            session.commit()
            session.close()
            bot.send_message(message.from_user.id, f"Введите примерную зарплату в рублях:", reply_markup=keyboard)
            return bot.register_next_step_handler(message, porashnaja_funkcia_dla_poiska_rabotnikov_3)
    except Exception as er:
        log(message=message, full=True, where="porashnaja_funkcia_dla_poiska_rabotnikov_2", comments=str(er))


def porashnaja_funkcia_dla_poiska_rabotnikov_3(message):
    try:
        log(message=message, where="porashnaja_funkcia_dla_poiska_rabotnikov_3")
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
            user.time = tconv(message.date)
            session.add(user)
            session.commit()
        update(message)
        if message.text == f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню":
            keyboard = keyboard_creator([["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
                                         "Расписание обучения"])
            bot.send_message(message.from_user.id, f"Что вас интересует?", reply_markup=keyboard)
            return bot.register_next_step_handler(message, vilka)
        else:
            govnolist = re.findall(r"\b\d+k*\b", str(message.text).replace("к", "k"))
            govnolist = [str(i).replace("k", "000") for i in govnolist]
            govnolist = list(map(int, govnolist))
            if govnolist == []:
                keyboard = keyboard_creator([f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню"])
                bot.send_message(message.from_user.id, f"Вы не ввели ЗП, попробуйте ещё раз.", reply_markup=keyboard)
                return bot.register_next_step_handler(message, porashnaja_funkcia_dla_poiska_rabotnikov_3)
            bot.send_message(message.from_user.id, f"Начинаем поиск(нет)",
                             reply_markup=buttons_creator(
                                 {f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню": "to start menu"}))
            list_poiska = machinazii_s_poiskom()
            key_dict = {"1": {"<": "back"}}
            user.arg3 = sum(govnolist) / len(govnolist)
            session.commit()
            text = f"Страница 1 из {len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1}\n\n"
            _list = []
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                string = f"{1 + i}. Профессия: {list_poiska[i].job}\n     Зарплата:    {list_poiska[i].salary}"
                _list.append(string)
            text += "\n".join(_list)
            key_dict["1"]["1"] = "1"
            key_dict["1"]["2"] = "2"
            key_dict["1"]["3"] = "3"
            key_dict["1"]["4"] = "4"
            key_dict["1"]["5"] = "5"
            key_dict["1"][">"] = "next"
            bot.send_message(message.from_user.id, text, reply_markup=buttons_creator(key_dict))
            return bot.register_next_step_handler(message, porasnij_poisk_rabochih)
            # return bot.register_next_step_handler(message, vilka, list_poiska)
    except Exception as er:
        log(message=message, full=True, where="porashnaja_funkcia_dla_poiska_rabotnikov_3", comments=str(er))


def porasnij_poisk_rabochih(message):
    try:
        log(message=message, where="porasnij_poisk_rabochih")
        # session = db_session.create_session()
        # keyboard = keyboard_creator([["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
        #                              "Расписание обучения"])
        # user = session.query(Ban).filter(Ban.tg_id == message.from_user.id).first()
        # try:
        #     if user.ban and user.count == 0:
        #         video = open("data/media/БАН.mp4", "rb")
        #         bot.send_message(message.from_user.id, "Вы забанены. Можете написать в поддержку",
        #                          reply_markup=types.ReplyKeyboardRemove())
        #         bot.send_video(message.from_user.id, video)
        #         user.count += 1
        #         session.commit()
        #         return bot.register_next_step_handler(message, get_text_messages)
        #     elif user.count != 0:
        #         return bot.register_next_step_handler(message, get_text_messages)
        # except Exception:
        #     user = Ban()
        #     user.tg_id = message.from_user.id
        #     user.ban = False
        #     user.count = 0
        #     user.time = tconv(message.date)
        #     session.add(user)
        #     session.commit()
        # update(message)
        # bot.send_message(message.from_user.id, f"ss", reply_markup=keyboard)
        # return bot.register_next_step_handler(message, vilka)
        if message.text == f"{emojize(SMILE[0], use_aliases=True)} Вернуться в меню":
            keyboard = keyboard_creator([["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
                                         "Расписание обучения"])
            bot.send_message(message.from_user.id, f"Что вас интересует?", reply_markup=keyboard)
            return bot.register_next_step_handler(message, vilka)
        return bot.register_next_step_handler(message, porasnij_poisk_rabochih)
    except Exception as er:
        log(message=message, full=True, where="porasnij_poisk_rabochih", comments=str(er))


def main_menu(message):
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
        user.time = tconv(message.date)
        session.add(user)
        session.commit()
    # log(message=message, where='main_menu')
    # answer = loginned(message)
    # try:
    #     answer = bool(answer)
    # except Exception:
    #     bot.send_message(message.from_user.id,
    #                      f"Ты забанен, теряйся клоун")
    #     return 0
    # if not answer:
    #     bot.send_message(message.from_user.id,
    #                      "Что тебе надо?")
    #     return bot.register_next_step_handler(message, main_menu)
    # else:
    #     return bot.register_next_step_handler(message, main_menu)


@bot.callback_query_handler(func=lambda call: call.data in ['1', '2', '3', '4', '5', 'next', 'back', 'to start menu'])
def callback_worker(call):
    if call.data == "back":
        text = call.message.text.split("\n")
        now_page = int(text[0].split()[1])
        if now_page - 1 >= 1:
            text[0] = f"Страница {now_page - 1} из {int(text[0].split()[3])}"
            key_dict = {"1": {"<": "back"}}
            key_dict["1"]["1"] = "1"
            key_dict["1"]["2"] = "2"
            key_dict["1"]["3"] = "3"
            key_dict["1"]["4"] = "4"
            key_dict["1"]["5"] = "5"
            key_dict["1"][">"] = "next"
            list_poiska = machinazii_s_poiskom()
            text = text[: 2]
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                text.append(
                    f"{1 + i}. Профессия: {list_poiska[5 * (now_page - 2) + i].job}\n     Зарплата:    {list_poiska[5 * (now_page - 2) + i].salary}")
            text = "\n".join(text)
        else:
            text[0] = f"Страница {int(text[0].split()[3])} из {int(text[0].split()[3])}"
            list_poiska = machinazii_s_poiskom()
            key_dict = {"1": {"<": "back"}}
            now_page = int(text[0].split()[3]) - 1
            for i in range((len(list_poiska) - 1) % 5 + 1):
                key_dict["1"][f"{1 + i}"] = f"{1 + i}"
            key_dict["1"][">"] = "next"
            text = text[: 2]
            for i in range((len(list_poiska) - 1) % 5 + 1):
                text.append(
                    f"{1 + i}. Профессия: {list_poiska[5 * now_page + i].job}\n     Зарплата:    {list_poiska[5 * now_page + i].salary}")
            text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "next":
        text = call.message.text.split("\n")
        now_page = int(text[0].split()[1])
        if now_page + 1 <= int(text[0].split()[3]):
            if now_page + 1 != int(text[0].split()[3]):
                text[0] = f"Страница {now_page + 1} из {int(text[0].split()[3])}"
                key_dict = {"1": {"<": "back"}}
                key_dict["1"]["1"] = "1"
                key_dict["1"]["2"] = "2"
                key_dict["1"]["3"] = "3"
                key_dict["1"]["4"] = "4"
                key_dict["1"]["5"] = "5"
                key_dict["1"][">"] = "next"
                list_poiska = machinazii_s_poiskom()
                text = text[: 2]
                for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                    text.append(
                        f"{1 + i}. Профессия: {list_poiska[5 * now_page + i].job}\n     Зарплата:    {list_poiska[5 * now_page + i].salary}")
                text = "\n".join(text)
            else:
                text[0] = f"Страница {now_page + 1} из {int(text[0].split()[3])}"
                list_poiska = machinazii_s_poiskom()
                key_dict = {"1": {"<": "back"}}
                for i in range((len(list_poiska) - 1) % 5 + 1):
                    key_dict["1"][f"{1 + i}"] = f"{1 + i}"
                key_dict["1"][">"] = "next"
                text = text[: 2]
                for i in range((len(list_poiska) - 1) % 5 + 1):
                    text.append(
                        f"{1 + i}. Профессия: {list_poiska[5 * now_page + i].job}\n     Зарплата:    {list_poiska[5 * now_page + i].salary}")
                text = "\n".join(text)
        else:
            text[0] = f"Страница 1 из {int(text[0].split()[3])}"
            key_dict = {"1": {"<": "back"}}
            key_dict["1"]["1"] = "1"
            key_dict["1"]["2"] = "2"
            key_dict["1"]["3"] = "3"
            key_dict["1"]["4"] = "4"
            key_dict["1"]["5"] = "5"
            key_dict["1"][">"] = "next"
            list_poiska = machinazii_s_poiskom()
            text = text[: 2]
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                text.append(f"{1 + i}. Профессия: {list_poiska[i].job}\n     Зарплата:    {list_poiska[i].salary}")
            text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "to start menu":
        keyboard = keyboard_creator([["Поиск работника", "Поиск работы"], "Оставить резюме", "Запись на обучение",
                                     "Расписание обучения"])
        bot.send_message(call.message.chat.id, f"Что вас интересует?", reply_markup=keyboard)
        return bot.register_next_step_handler(call.message, vilka)
    else:
        session = db_session.create_session()
        text = call.message.text.split("\n")
        now_page = int(text[0].split()[1])
        text = []
        nomer = (now_page - 1) * 5 + int(call.data)
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        _list = machinazii_s_poiskom()
        chelik = session.query(People).filter(People.id == _list[nomer - 1].id).first()
        text.append(f"{chelik.job}")
        text.append("")
        text.append(f"Ожидаемая зарплата: {chelik.salary}")
        text.append(f"Занятость: {chelik.employment}")
        text.append("")
        text.append(f"Опыт работы: {chelik.experience if len(chelik.experience) <= 250 else f'{chelik.experience[: 250]}(Подробнее в полном резюме)'}")
        buttons = buttons_creator({"1": {
            f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return',
            'Контакты': 'cont',
            'Полное резюме': 'full'
        }})
        text = "\n".join(text)
        user.count = (now_page - 1) * 5 + int(call.data)
        session.commit()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
        # print(f"\033[0m{call.message.text}")


@bot.callback_query_handler(func=lambda call: call.data in ['return', 'cont', 'full', "about"])
def callback2(call):
    if call.data == 'return':
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        list_poiska = machinazii_s_poiskom()
        key_dict = {"1": {"<": "back"}}
        text = call.message.text.split("\n")
        nomer = user.count
        text = [
            f"Страница {nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1} из {len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1}",
            ""]
        for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
            nomer1 = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            string = f"{1 + i}. Профессия: {list_poiska[nomer1 * 5 + i].job}\n     Зарплата:    {list_poiska[nomer1 * 5 + i].salary}"
            text.append(string)
        text = "\n".join(text)
        key_dict["1"]["1"] = "1"
        key_dict["1"]["2"] = "2"
        key_dict["1"]["3"] = "3"
        key_dict["1"]["4"] = "4"
        key_dict["1"]["5"] = "5"
        key_dict["1"][">"] = "next"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "about":
        session = db_session.create_session()
        user = session.query(Ban).filter(Ban.tg_id == call.message.chat.id).first()
        text = call.message.text.split("\n")
        text = []
        nomer = user.count
        _list = machinazii_s_poiskom()
        chelik = session.query(People).filter(People.id == _list[nomer - 1].id).first()
        text.append(f"{chelik.job}")
        text.append("")
        text.append(f"Ожидаемая зарплата: {chelik.salary}")
        text.append(f"Занятость: {chelik.employment}")
        text.append("")
        text.append(
            f"Опыт работы: {chelik.experience if len(chelik.experience) <= 250 else f'{chelik.experience[: 250]}(Подробнее в полном резюме)'}")
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
        text = call.message.text.split("\n")
        text = []
        nomer = user.count
        text.append("Вот контактная информация:")
        text.append("")
        _list = machinazii_s_poiskom()
        chelik = session.query(People).filter(People.id == _list[nomer - 1].id).first()
        text.append(f"ФИО: {chelik.name}")
        text.append(f"Номер телефона: {chelik.phone}")
        text.append(f"Адрес электронной почты: {chelik.mail}")
        text = "\n".join(text)
        buttons = buttons_creator({'1': {f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'about'}})
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)
    elif call.data == 'full':
        session = db_session.create_session()
        text = ["это не робит, пока что"]
        text = "\n".join(text)
        buttons = buttons_creator({'1': {f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'about'}})
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

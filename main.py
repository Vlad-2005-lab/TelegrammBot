import telebot
from telebot import types
from data.people import People
from data.boss import Boss
from data import db_session
import time
import datetime

bot = telebot.TeleBot('1625541968:AAF0Hrv_57dx8x1osP56CxnxSejWu-kWijc')
print('\033[35mStarting.....')
count = -1
history = True
print('\033[35mConnecting to db....')
db_session.global_init("db/data.sqlite")
print('\033[35mDb was conected...')


def log(message=None, where='ne napisal', full=False, comments="None"):
    global count, history
    count += 1
    if history:
        history = False
        print("""\033[33mWriting history started:\033[30m""")
    elif full:
        try:
            print(f"""\033[33m{"-" * 100}
log №{count}
from: {where}
full: {full}
id: \033[36m{message.from_user.id}\033[33m
username: \033[36m{message.from_user.username}\033[33m
first_name(имя): \033[36m{message.from_user.first_name}\033[33m
last_name(фамилия): \033[36m{message.from_user.last_name}\033[33m
text: {message.text}
message: \033[35m{message}\033[33m""")
        except Exception as er:
            print(f"""\033[31m{"-" * 100}\n!ошибка, лог №{count}\n message: {message}
where: {where}
full: {full}\033
comments: {comments}
error: {er}[30m""")
    else:
        try:
            print(f"""\033[33m{"-" * 100}
log №{count}
from: {where}
full: {full}
id: \033[36m{message.from_user.id}\033[33m
username: \033[36m{message.from_user.username}\033[33m
first_name(имя): \033[36m{message.from_user.first_name}\033[33m
last_name(фамилия): \033[36m{message.from_user.last_name}\033[33m
text: \033[35m{message.text}\033[33m
comment: {comments}\033[30m""")
        except Exception as er:
            print(f"""\033[31m!ошибка! Лог №{count}\n message: {message}
where: {where}
full: {full}
comments: {comments}
error: {er}\033[30m""")


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


def buttons_creator(dict_of_names):
    returned_k = types.InlineKeyboardMarkup()
    for i in dict_of_names.keys():
        exec(f"""button = types.InlineKeyboardButton(text='{i}', callback_data='{dict_of_names[i]}')""")
        exec(f"""returned_k.add(button)""")
    return returned_k


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


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
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

        pass
    except Exception as er:
        log(message=message, where="get_text_messages", comments=str(er))


def main_menu(message):
    pass
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


# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     if call.data == "s1":
#         keyboard = buttons_creator({"Согласен": "s2",
#                                     "Нет": "s3"})
#         bot.send_message(call.from_user.id, "Добрый день, предлагаю вам указать свои данные", reply_markup=keyboard)
#     else:
#         print(f'\033[31m!ошибка!\nстрока: 51\033[30m\ncall.data: {call.data}')


while True:
    try:
        print('\033[30mStarted.....')
        log()
        exec('bot.polling(none_stop=True, interval=0)')
    except Exception:
        print('\033[31mCrashed.....')
        time.sleep(10)
        print('\033[35mRestarting.....')

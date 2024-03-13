import telebot
from telebot import types
import random


token = "7105493880:AAEcctHsDe22IlHOvAGEWGHLcjgVnLwssrA"
bot = telebot.TeleBot(token)

questions_base = [
    ["Какой язык программирования называется в честь змеи?", "Python", ["Snake", "Cobra", "Python", "Piton"]],
    ["Какая фирма имеет \"Яблочное\" название?", "Apple", ["AppleJuice","Apple", "RedApple", "GreenApple"]],
    ["Российский видеохостинг", "Rutube", ["Youtube", "Vimeo", "Instagram", "Rutube"]],
    ["Сколько жизней у кошек?", "9", ["7", "5", "12", "9"]],
    ["Какое \"погоняло\" у Никиты Киргинцева?", "Газпром", ["Транснефть", "Газпром", "Роснефть", "Топлайн"]],
    ["Самый топовый ВУЗ?", "Политех", ["ОмГУ","СибАДИ", "ОмГУПС", "Политех"]]



]

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text="Начать!")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Привет! Хочешь сыграть в игру \"Кто хочет стать миллионером?\"',
                     reply_markup=markup)


answers = []
correct_answerr = "NCA"
is_game_started = False
balance = 0
reward = 1000

@bot.message_handler(content_types=['text'])
def message_reply(message):
    global correct_answerr
    global answers
    global is_game_started
    global balance
    global reward
    if message.text == "Начать!" or message.text == "Сыграть заново":
        get_new_question(message)
        is_game_started = True
    if is_game_started:
        if message.text == correct_answerr:
            bot.send_message(message.chat.id, f"Правильный ответ! Вы зарабатываете {reward} руб!")
            balance += reward
            reward *= 2
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(text="Продолжить"))
            markup.add(types.KeyboardButton("Закончить игру и забрать сумму"))
            bot.send_message(message.chat.id, f"Желаете продолжить или забрать сумму {balance} руб?", reply_markup=markup)
        elif message.text == "Продолжить":
            get_new_question(message)
        elif message.text == "Закончить игру и забрать сумму":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(text="Сыграть заново"))
            bot.send_message(message.chat.id, f"Поздравляем! Вы выиграли {balance} руб!")
            bot.send_message(message.chat.id, "Хотите сыграть заново?", reply_markup=markup)
            balance = 0
            reward = 1000
            is_game_started = False
        else:
            for answ in answers:
                if message.text == answ:
                    bot.send_message(message.chat.id, f"К сожалению вы ответили неправильно и вся ваша сумма: {balance} руб сгорает!")
                    balance = 0
                    reward = 1000
                    is_game_started = False
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(types.KeyboardButton(text="Сыграть заново"))
                    bot.send_message(message.chat.id, "Сыграть заново?", reply_markup=markup)




def get_new_question(message):
    global correct_answerr
    global answers
    global balance

    number = random.randint(0, 5)
    quest = questions_base[number]
    question = quest[0]
    correct_answerr = quest[1]
    answers = quest[2]

    bot.send_message(message.chat.id, f'Ваш баланс: {balance} \nНаграда за вопрос: {reward}')
    bot.send_message(message.chat.id, 'Внимание вопрос...')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for answer in answers:
        markup.add(types.KeyboardButton(text=answer))

    bot.send_message(message.chat.id, question, reply_markup=markup)


bot.infinity_polling()

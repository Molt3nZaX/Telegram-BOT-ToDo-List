import telebot
from random import choice

# $ pip install pyTelegramBotAPI

token = ''

bot = telebot.TeleBot(token)

help_notification = '''
/help - Вывести список доступных команд
/add 'Дата' 'Задача' - Добавить задачу в список
/show 'Дата' - Вывести задачи, запланированные на эту 'Дату'
/show_all - Вывести все запланированные задачи
/random - случайная задача на сегодня
'''

todos = dict()
RANDOM_TASKS = ['Погулять', 'Покататься на велосипеде', 'Почитать любимую книгу',
                'Сходить на скалодром']


def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, help_notification)


@bot.message_handler(commands=['random'])
def random(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача "{task}" добавлена на "Cегодня"')


@bot.message_handler(commands=['add'])
def add(message):
    _, date, tail = message.text.split(maxsplit=2)
    task = ' '.join([tail])
    # TODO: 1
    if len(task) < 3:
        bot.send_message(message.chat.id, 'Задачи должны быть больше 3х символов')
    else:
      add_todo(date, task)
      bot.send_message(message.chat.id, f'Задача "{task}" добавлена на дату "{date}"')


@bot.message_handler(commands=['show'])
def print_(message):
    # TODO: 2
    dates = message.text.split(maxsplit=1)[1].lower().split()
    response  = ''
    for date in dates:
        tasks = todos.get(date)
        response += f'{date.upper()}: \n'
        for task in tasks:
            response += f'- {task}\n'
        response += '\n'
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['show_all'])
def print_(message):
    response  = ''
    for date in todos:
        tasks = todos.get(date)
        response += f'{date.upper()}: \n'
        for task in tasks:
            response += f'- {task}\n'
        response += '\n'
    bot.send_message(message.chat.id, response)

bot.polling(none_stop=True)

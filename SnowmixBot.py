import re
import telebot
import random
import requests
from bs4 import BeautifulSoup
from telebot import types
from tokenfile import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['shani'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    random_sender = types.KeyboardButton('Шани, скинь рандомное число')
    markup.add(random_sender)
    dice_roller = types.KeyboardButton('Dice')
    markup.add(dice_roller)
    bot.send_message(message.chat.id, '<b>Мурнерэйтор Кэт Мяутивэйтед</b> (Мяу-бип-мур-пиип)', parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'шани, скинь рандомное число':
        msg = bot.send_message(message.chat.id, 'Напиши начало диапазона', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, second_number_step)
    elif message.text.lower() == 'dice':
        msg = bot.send_message(message.chat.id, 'Какой кубик?', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, dice_type)
    elif message.text.lower() == 'привет, шани':
        bot.send_message(message.chat.id, 'Здарова, чур не я!')
    elif message.text == '/help' or message.text == '/start':
        bot.send_message(message.chat.id, 'Напиши \'Привет, Шани\', на большее ты не способен...\nЕсли покормишь меня'
                                          ', то можем шифтануться!  /shani')
    elif message.text == 'лол':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAPDYyJMrIKxUT40JQKFuOGLdXGWIOQAAiQDAAK1cdoGn4orPORRz70pBA')
    elif message.text == 'за что?':
        bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAPGYyJM8spf9iWneAF1k_3gFkWyOhYAAhIBAAJxffwUM1GVhD_xC3IpBA')
    elif message.text.lower() == 'мяу' or message.text.lower() == 'мур':
        bot.send_message(message.chat.id, 'Ты втираешь мне какую-то дичь, тебе явно нужна /help')
    elif message.text.lower() == 'шани, выключи клаву':
        bot.send_message(message.chat.id, 'Уже', reply_markup=types.ReplyKeyboardRemove())
    elif message.text.lower() == 'шани, расскажи анекдот':
        joke_telling(message)
    else:
        pass


@bot.message_handler(content_types=['photo'])
def photo_react(message):
    bot.send_message(message.chat.id, 'Красивое')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


# Jokes
def joke_telling(message):
    url = 'https://www.anekdot.ru/random/anekdot/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quote = soup.find('div', class_='text')
    print(quote)
    filter_div = re.sub(r'<div class="text">|</div>', '', str(quote))
    sub = re.sub(r'<br/>', '\n', filter_div)
    filter_enters = re.sub(r'([А-Яа-яЁё,.])\s*\n\s*([А-Яа-яЁё])', r'\1 \2', sub)
    bot.send_message(message.chat.id, filter_enters)


def any_dice(x):
    for element in [4, 6, 8, 10, 12, 20, 100]:
        if element == x:
            return True


def dice_type(message):
    try:
        num_dice = int(message.text)
        if any_dice(num_dice):
            if num_dice == 20:
                dice_result = random.randint(1, num_dice)
                if dice_result >= 15:
                    bot.send_message(message.chat.id, 'Вот это повезло!\n' + str(dice_result))
                else:
                    bot.send_message(message.chat.id, 'Ну такое...\n' + str(dice_result))
            else:
                bot.send_message(message.chat.id, 'Ахалай-мяухалай:  ' + str(random.randint(1, num_dice)))
        else:
            bot.send_message(message.chat.id, 'Нет такого кубика! В следующий раз выбирай УМОМ:'
                                              ' 4, 6, 8, 10, 12, 20, 100')
    except ValueError:
        bot.send_message(message.chat.id, 'Ага, рассказывай...')


def second_number_step(message):
    global num_first
    try:
        num_first = int(message.text)
        msg = bot.send_message(message.chat.id, 'А конец?')
        bot.register_next_step_handler(msg, result_number_step)
    except ValueError:
        bot.send_message(message.chat.id, 'Ага, рассказывай...')


def result_number_step(message):
    global num_second
    try:
        num_second = int(message.text)
        if num_first == num_second:
            bot.send_message(message.chat.id, 'Ты че, мяурак? Явно не ' + str(num_second))
        elif num_second < num_first:
            bot.send_message(message.chat.id, 'Ты явно плохо разбираешься в мяутематике.\nХорошо, что я хорошо:3')
            result2(message)
        else:
            result1(message)
    except ValueError:
        bot.send_message(message.chat.id, 'Ага, рассказывай...')


def result1(message):
    bot.send_message(message.chat.id, 'Ахалай-мяухалай:  ' + str(random.randint(num_first, num_second)))


def result2(message):
    bot.send_message(message.chat.id, 'Ахалай-мяухалай:  ' + str(random.randint(num_second, num_first)))


bot.polling(none_stop=True, interval=0)

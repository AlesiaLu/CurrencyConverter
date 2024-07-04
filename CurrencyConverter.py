import telebot

from config import currencies, TOKEN
from exceptions import APIException, Converter

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f'Привет!\n'
    text += 'Я бот-конвертер валют.\n'
    text += 'Нажмите /help, чтобы увидеть инструкции.\n'
    text += 'Нажмите /currencies, чтобы увидеть доступные валюты.\n'
    text += 'Нажмите /convert для конвертации.'
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert' , 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду в следующем формате (через пробел):' \
           ' \n- Название валюты, из которой конвертируем  \n- Название валюты, в которую конвертируем \n- Количество первой валюты, используя цифры\n \
 Список доступных валют: /currencies'
    bot.reply_to(message, text)

@bot.message_handler(commands=['currencies'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Необходимо ввести 3 (три) параметра')
        base, quote, base_amount = values
        total_base_amount = Converter.convert(base, quote, base_amount)
    except APIException as e:
        bot.reply_to(message, f'Неверно введены параметры. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка. Попробуйте еще раз \n{e}')

    else:
        text = f'Цена {base_amount} {base} в {quote}: {total_base_amount}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)



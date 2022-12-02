import telebot
from pycoingecko import CoinGeckoAPI
from config import TOKEN, exchanges

bot = telebot.TeleBot(TOKEN)
api = CoinGeckoAPI()


# Обработка команды старт
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, f"Приветствую тебя, {message.chat.username}!")
    bot.send_message(message.chat.id, "😊")
    bot.send_message(message.chat.id, "Для получения информации и списка команд вводи /help.")


# Обработка команды help
@bot.message_handler(commands=['help'])
def handle_start(message):
    bot.send_message(message.chat.id, "Для конвертации введите через запятую в одну строку: \nИмя валюты, цену на которую надо узнать, имя валюты, цену в которой надо узнать и количество переводимой валюты. \nВалюта вводится на английской раскладке.")


# Обработка значений валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


# Получение курса валют
@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        command_message = message.text.split()
        # Проверка несоответствия передачи параметров.
        if len(command_message) != 3:
            raise ValueError("Неверное количество параметров!")
        base, quote, amount = command_message
        currency = api.get_price(ids=base, vs_currencies=quote)[base][quote]
        convert = currency * float(amount)
        bot.reply_to(message, f"Цена {amount} {base} в {quote} составляет: {convert}")
    except ValueError as e:
        bot.reply_to(message, f"Ошибка в команде. \n{e}")


# Проверка и запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)

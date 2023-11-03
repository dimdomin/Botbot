import telebot
from dotenv import load_dotenv
import  os
from extention import APIConverter, Cryptoconverter
from config import cash
load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text= f"Приветствую {message.chat.username}! \n Добро пожаловать в бот конвертер валют! \n \
    Чтобы начать работу введите команду боту в следующем формате: \n <название валюты> \
<в какую валюту перевести> \
<сумма переводимой валюты> \n увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text= "Доступные валюты:"
    for key in cash.keys():
        text = '\n'.join((text,key, ))
    bot.reply_to(message, text)
@bot.message_handler(commands=['stop']) #В списке вы можете указать любые команды, на эти команды бот будет обращаться к функции stop() - ['start','stop',...]
def stop(message):
    bot.send_message(message.chat.id,'Бот остановлен')
    bot.stop_bot()



@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIConverter("Слишком много переменных")

        quote, base, amount = values
        total_base = Cryptoconverter.convert(quote, base, amount)
    except APIConverter as e:
            bot.reply_to(message, f"Ошибка пользователя! \n {e}")
    except Exception as e:
            bot.reply_to(message, f"Не удалось обработать команду \n {e}")
    else:

        rur=f"{float(total_base) * float(amount)}"
        text = f"Цена {amount} {quote} в {base} - {round(float(rur),2)}"
        bot.send_message(message.chat.id, text)

bot.polling()








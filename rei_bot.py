# Telegram bot. Just for testing.
import telebot
import requests

token = "235398494:AAFEZ2elV6pZDXwV3KX0auMQkthOa3G2c9M"
bot = telebot.TeleBot(token)

REI = "http://static.zerochan.net/Ayanami.Rei.full.266985.jpg"
# f = open("rei.jpg", "wb")
# f.write(requests.get(rei).content)
# f.close()


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, """
/help
/rei
<any_text>""")


@bot.message_handler(commands=['rei'])
def ayanami(message):
    if message.text.startswith("/rei"):
        for i in reversed(range(1, 6)):
            bot.send_message(message.chat.id, str(i))
        img = open("rei.jpg", "+b")
        img.write(requests.get(REI).content)
        bot.send_photo(message.chat.id, img)
        img.close()


@bot.message_handler(func=lambda message: (message.text != "/start" and message.text != "/help" and message.text != "/rei"), content_types=["text"])
def repeat(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
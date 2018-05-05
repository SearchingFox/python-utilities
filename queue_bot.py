from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter
import telegram
# import logging

updater = Updater(token="")
dispatcher = updater.dispatcher
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
queue_file = ""
main_keyboard = [["В очередь!"], ["А кто последний?"], ["Отменить запись."]]


class FilterQueue(BaseFilter):
    def filter(self, message):
        return "В очередь!" in message.text

class FilterDigit(BaseFilter):
    def filter(self, message):
        return message.text.isdigit()

class FilterList(BaseFilter):
    def filter(self, message):
        return "А кто последний?" in message.text

class FilterCancel(BaseFilter):
    def filter(self, message):
        return "Отменить запись." in message.text

class FilterBack(BaseFilter):
    def filter(self, message):
        return "<-" in message.text


def start(bot, update):
    reply_markup = telegram.ReplyKeyboardMarkup(main_keyboard)
    bot.send_message(chat_id=update.message.chat_id, text="В очередь, сукины дети, в очередь!!!", reply_markup=reply_markup)


def choose_number(bot, update):
    uid = str(update.message.from_user.id)

    with open(queue_file, 'r') as f:
        used = [i.split('^')[0] for i in f.readlines()]

    if any([uid == i for i in used]):
        update.message.reply_text("Вы уже в очереди.")
        return

    digits_keyboard = [['1', '2', '3', '4', '5'], ['6', '7', '8', '9','10'], ['11', '12', '13', '14', '<-']]
    reply_markup = telegram.ReplyKeyboardMarkup(digits_keyboard)
    bot.send_message(chat_id=update.message.chat_id, text="Какой номер в очереди хотите?", reply_markup=reply_markup)


def add_to_queue(bot, update):
    with open(queue_file, 'r', encoding='utf-8') as f:
        used = {}
        for i in f.readlines():
            used[i.split('^')[0]] = int(i.split('^')[2])

    try:
        i = int(update.message.text)
    except Exception:
        update.message.reply_text("Это не число. Введите число.")
        return

    uid = str(update.message.from_user.id)
    fn = update.message.from_user.first_name
    ln = update.message.from_user.last_name

    if any([uid == i for i in used.keys()]):
        update.message.reply_text("Вы уже в очереди.")
        return
    if i in used.values():
        update.message.reply_text("Простите, но место уже занято.")
        return
    if i <= 0:
        update.message.reply_text("Номер должен быть больше нуля.")
        return

    if not fn:
        fn = ""
    if not ln:
        ln = ""

    username = fn + ' ' + ln
    if username == " ":
        username = uid

    with open(queue_file, 'a', encoding='utf-8') as f:
        f.write(uid + '^' + username + '^' + str(i) + '\n')

    reply_markup = telegram.ReplyKeyboardMarkup(main_keyboard)
    bot.sendMessage(update.message.chat_id, uid + ' - ' + username + ' - ' + str(i), reply_markup=reply_markup)


def print_queue(bot, update):
    with open(queue_file, 'r', encoding='utf-8') as f:
        str_queue = ""
        queue = {}
        for i in f.readlines():
            tok = i.split('^')
            queue[tok[2]] = tok[1]
        for key in sorted(queue.keys()):
            str_queue += key[:-1] + '. ' + queue[key]

    if str_queue != "":
        bot.send_message(chat_id=update.message.chat_id, text=str_queue)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Да нет пока никого.")


def delete_from_queue(bot, update):
    uid = str(update.message.from_user.id)

    with open(queue_file, 'r', encoding='utf-8') as f:
        queue = [i for i in f.readlines() if uid not in i]
    with open(queue_file, 'w', encoding='utf-8') as f:
        f.write("".join(queue))
    bot.send_message(chat_id=update.message.chat_id, text="Вы удалены из очереди.")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(FilterQueue(), choose_number))
dispatcher.add_handler(MessageHandler(FilterDigit(), add_to_queue))
dispatcher.add_handler(MessageHandler(FilterList(), print_queue))
dispatcher.add_handler(MessageHandler(FilterCancel(), delete_from_queue))
dispatcher.add_handler(MessageHandler(FilterBack(), start))

updater.start_polling()

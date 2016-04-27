import telegram
from telegram.ext import Updater
from settings import settings
from telegram.ext import CommandHandler
my_settings = settings.get('Homebot')
token = my_settings['token']
chat_id = my_settings['chat_id'];
updater = Updater(token=token)
dispatcher = updater.dispatcher
jobs = updater.job_queue
updater.start_polling()
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
def test(bot, update):
    custom_keyboard = [[ telegram.KeyboardButton(telegram.Emoji.THUMBS_UP_SIGN),telegram.KeyboardButton(telegram.Emoji.THUMBS_DOWN_SIGN) ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    results = bot.sendMessage(chat_id=update.message.chat_id, text="Test", reply_markup=reply_markup)
    print results
def job2(bot):
    reply_markup = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=chat_id, text='A single message with 30s delay',reply_markup=reply_markup)
start_handler = CommandHandler('start', start)
dispatcher.addHandler(start_handler)
test_handler = CommandHandler('test', test)
dispatcher.addHandler(test_handler)
jobs.put(job2, 30, repeat=False)
import telegram
from telegram.ext import Updater
from settings import settings
from telegram.ext import CommandHandler
token = settings.get('Homebot')['token']
updater = Updater(token=token)
dispatcher = updater.dispatcher
updater.start_polling()
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
def test(bot, update):
    custom_keyboard = [[ telegram.KeyboardButton(telegram.Emoji.THUMBS_UP_SIGN),telegram.KeyboardButton(telegram.Emoji.THUMBS_DOWN_SIGN) ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    results = bot.sendMessage(chat_id=update.message.chat_id, text="Test", reply_markup=reply_markup)
    print results
start_handler = CommandHandler('start', start)
dispatcher.addHandler(start_handler)
test_handler = CommandHandler('test', test)
dispatcher.addHandler(test_handler)
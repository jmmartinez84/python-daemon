import telegram
from telegram.ext import Updater
from settings import settings
token = settings.get('Homebot')['token']
updater = Updater(token=token)
dispatcher = updater.dispatcher
updater.start_polling()
def test(bot, update):
    custom_keyboard = [[ telegram.KeyboardButton(telegram.Emoji.THUMBS_UP_SIGN),telegram.KeyboardButton(telegram.Emoji.THUMBS_DOWN_SIGN) ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    results = bot.sendMessage(chat_id=update.message.chat_id, text="Test", reply_markup=reply_markup)
    print results
dispatcher.addTelegramCommandHandler('test', test)
import telegram
from telegram.ext import Updater
from settings import settings
token = settings.get('Homebot')['token']
updater = Updater(token=token)
dispatcher = updater.dispatcher
updater.start_polling()
def test(bot, update):
    results = bot.sendMessage(chat_id=update.message.chat_id, text="Test", reply_markup={"keyboard":[["Test1"], ["Test2"], ["Test3"], ["Test4"]})
    print results
dispatcher.addTelegramCommandHandler('test', test)
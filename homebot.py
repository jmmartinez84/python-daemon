#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram
from telegram.ext import Updater
from settings import settings
from telegram.ext import CommandHandler
from DjangoRestClient import DjangoRestClient
credentials = settings.get('DjangoREST')
my_settings = settings.get('Homebot')
token = my_settings['token']
chat_id = my_settings['chat_id'];
updater = Updater(token=token)
dispatcher = updater.dispatcher
jobs = updater.job_queue
updater.start_polling()
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
def wifi(bot, update):
    custom_keyboard = [[ telegram.KeyboardButton("On"),telegram.KeyboardButton("Off"), telegram.KeyboardButton("Cancel") ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,  resize_keyboard = True, one_time_keyboard=True)
    results = bot.sendMessage(chat_id=update.message.chat_id, text="Wifi:", reply_markup=reply_markup)
    print results
def job_alerts(bot):
    drc = DjangoRestClient(credentials['url'], credentials['user'], credentials['pwd'])
    alerts = drc.get_alerts_not_sent()
    for alert in alerts:
        bot.sendMessage(chat_id=chat_id, text=alert['alert_text'])
        drc.set_alert_as_sent(alert)
start_handler = CommandHandler('start', start)
dispatcher.addHandler(start_handler)
wifi_handler = CommandHandler('wifi', wifi)
dispatcher.addHandler(wifi_handler)
jobs.put(job_alerts, 5*60)
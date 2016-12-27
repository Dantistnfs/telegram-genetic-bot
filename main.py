#!/usr/bin/env python
import os
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler

updater = Updater(token=os.environ['TELEGRAM_BOT_API_KEY'])
dispatcher = updater.dispatcher
rt_dict = {'A':'T','T':'A','G':'C','C':'G'}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def ReverseTranscription(bot, update, args):
    seq = ' '.join(args).upper()
    for base in seq:
        if base not in 'ATCG':
            bot.sendMessage(chat_id=update.message.chat_id, text="Error: NOT a DNA sequence")
            return 0

    text_for_rt = "".join([rt_dict[base] for base in reversed(seq)])
    bot.sendMessage(chat_id=update.message.chat_id, text=text_for_rt)



start_handler = CommandHandler('start', start)
RT_handler = CommandHandler('RT', ReverseTranscription, pass_args=True)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(RT_handler)

updater.start_polling()



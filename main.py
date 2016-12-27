#!/usr/bin/env python
import os
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler


import eutils.client
ec = eutils.client.Client()

updater = Updater(token=os.environ['TELEGRAM_BOT_API_KEY'])
dispatcher = updater.dispatcher
rt_dict = {'A':'T','T':'A','G':'C','C':'G','N':'N','R':'Y','Y':'R'}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

bot_starting_message = "Hi i'm telegram bot and your personal assistant, more info with \"\\help\" command"
bot_help_meggase = "Help is still in development."


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=bot_starting_message)


def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=bot_help_meggase)


def ReverseTranscription(bot, update, args):
    seq = ' '.join(args).upper()
    for base in seq:
        if base not in 'ATCGN':
            bot.sendMessage(chat_id=update.message.chat_id, text="Error: NOT a DNA sequence")
            return 0

    text_for_rt = "".join([rt_dict[base] for base in reversed(seq)])
    bot.sendMessage(chat_id=update.message.chat_id, text=text_for_rt)

def GeneSearcher(bot, update, args):
    gene = ' '.join(args).lower()
    egs = ec.efetch(db='gene', term=gene)
    bot.sendMessage(chat_id=update.message.chat_id, text=egs)

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
RT_handler = CommandHandler('RT', ReverseTranscription, pass_args=True)
Gene_search_handler = CommandHandler('gene', GeneSearcher, pass_args=True)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(RT_handler)
dispatcher.add_handler(Gene_search_handler)

updater.start_polling()



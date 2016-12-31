#!/usr/bin/env python
import os
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from Bio import Entrez
from handlers.ncbi.SearchGeneNCBI import * 
from handlers.sequence_ocr.sequence_ocr_handler import *


Entrez.email = "s.v.zubenko@imbg.org.ua" 

import eutils.client
import mahotas
ec = eutils.client.Client()

updater = Updater(token=os.environ['TELEGRAM_BOT_API_KEY'])
version = os.environ.get('HEROKU_RELEASE_VERSION')
relase_time = os.environ.get('HEROKU_RELEASE_CREATED_AT')
rt_dict = {'A':'T','T':'A','G':'C','C':'G','N':'N','R':'Y','Y':'R'}

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

bot_starting_message = "Hi, %s. I'm telegram bot and your personal assistant, more info with \"/help\" command"
bot_help_meggase = "Help is still in development. But you can try to use some functions: \n/entrezid [id];\n /rt [DNAseq];\n /ncbigene [GENE];\n /ocr_sequence. \n Made by @dantistnfs, version: " + str(version) + "\n Deployed: " + str(relase_time) + "\n Mahotas version: " + str(mahotas.__version__)


def start(bot, update):
    user = update.message.from_user
    bot.sendMessage(chat_id=update.message.chat_id, text=(bot_starting_message % user.first_name))


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

def EntrezID(bot, update, args):
    gene = ' '.join(args)
    try:
        int(gene)
    except ValueError:
        bot.sendMessage(chat_id=update.message.chat_id, text="Error: NOT a ENTREZ ID")
        return 0
    try:
        egs = ec.efetch(db='gene', id=gene)
        eg = egs.entrezgenes[0]
        answer = ' '.join([str(eg.hgnc), str(eg.maploc), str(eg.description), str(eg.type), str(eg.genus_species),'\n'])
    except TypeError:
        bot.sendMessage(chat_id=update.message.chat_id, text="Error: NOT such GENE")
        return 0
    bot.sendMessage(chat_id=update.message.chat_id, text=answer)





start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
RT_handler = CommandHandler('rt', ReverseTranscription, pass_args=True)
Entrezid_handler = CommandHandler('entrezid', EntrezID, pass_args=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(RT_handler)
dispatcher.add_handler(Entrezid_handler)
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(ocr_conv_handler)

updater.start_polling()



from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from Bio import Entrez

ORGANISM = range(1)


def chooseorganismtostart(bot, update, args, user_data):
    reply_keyboard = [['Anyone'],['Human'],['Escherichia coli'],['Cypripedioideae']]
    user_data['gene'] = ' '.join(args)
    if user_data['gene'] == '':
        bot.sendMessage(chat_id=update.message.chat_id, text="Hey, you didn't specify gene to search for")
        return ConversationHandler.END
    update.message.reply_text('Please choose organism where to serach',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))        
    return ORGANISM


def ncbisearch(bot, update, user_data):
    user = update.message.from_user
    choosed_organism = update.message.text
    if choosed_organism == 'Other':
        search_line = user_data['gene']
    else:
        search_line = choosed_organism + "[Orgn] AND " + user_data['gene'] + "[Gene]"
    handle = Entrez.esearch(db="nucleotide", term=search_line)
    record = Entrez.read(handle)
    handle.close()
    try:
        record["IdList"][0] == True
    except IndexError:
        bot.sendMessage(chat_id=update.message.chat_id, text=("Sorry, but i didn't found anything for this search query: \n %s " % search_line))
        return ConversationHandler.END
    handle_nucleotide = Entrez.efetch(db="nucleotide", id=record["IdList"][0], rettype="gb", retmode="xml")
    gene_record = Entrez.read(handle_nucleotide)
    bot.sendMessage(chat_id=update.message.chat_id, text=gene_record[0]["GBSeq_definition"])
    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Sorry if i made something wrong( \n However, if you think it\'s bug, or you have idea how to make me better, write to my creator: @dantistnfs',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('ncbigene', chooseorganismtostart, pass_args=True, pass_user_data=True)],

    states={
        ORGANISM: [RegexHandler('^(Cypripedioideae|Other|Escherichia coli|human)$', ncbisearch, pass_user_data=True)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

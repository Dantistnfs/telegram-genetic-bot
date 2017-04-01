from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from Bio import Entrez
import mygene

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
    mg = mygene.MyGeneInfo()
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
    response = gene_record[0]["GBSeq_definition"]
    file_s = open("temp.txt", "w")
    file_s.write(str(gene_record[0]))
    output = mg.query('symbol:' + str(user_data['gene']), species='human')
    response += " \nLocus: " + gene_record[0]['GBSeq_locus']
    response += " \nGBSeq primary code: " + gene_record[0]['GBSeq_primary-accession']
    try:
        response += " \nEnterezID: " + str(output['hits'][0]['entrezgene']) + "\nProbability of right entrezid: " + str(output['max_score']) + " %\nFor now, entrezid is searched only for Homo Sapiens! \nYou can check entrezid with /entrezid function."
    except Exception:
        response += " \nSorry, but entrezid not found."
    bot.sendMessage(chat_id=update.message.chat_id, text=response)
    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Sorry if i made something wrong( \n However, if you think it\'s bug, or you have idea how to make me better, write to my creator: @dantistnfs',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('ncbigene', chooseorganismtostart, pass_args=True, pass_user_data=True)],

    states={
        ORGANISM: [RegexHandler('^(Cypripedioideae|Anyone|Escherichia coli|Human)$', ncbisearch, pass_user_data=True)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

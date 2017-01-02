from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, RegexHandler)

from scihub import SciHub

sh = SciHub()

DOWNLOAD = range(1)

def scihub_search(bot, update, args, user_data):
    search_line = str(' '.join(args))
    results = sh.search(search_line, 10)
    user_data['results'] = results
    if len(results['papers']) == 0:
    	update.message.reply_text('Sorry, nothing found')
    else:
    	update.message.reply_text('Found: %d articles' % (len(results['papers'])))
    	for i in range(0,len(results['papers'])):
    		update.message.reply_text('%d. %s' %(i, results['papers'][i]['name']))
    	update.message.reply_text('Please, choose number of article you need.')
    return DOWNLOAD


def scihub_retrive(bot, update, user_data):
    user = update.message.from_user
    choosed_article = int(update.message.text)

    sh.download(user_data['results']['papers'][choosed_article]['url'])
    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Sorry if i made something wrong( \n However, if you think it\'s bug, or you have idea how to make me better, write to my creator: @dantistnfs',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('scihub', scihub_search, pass_args=True, pass_user_data=True)],

    states={
        DOWNLOAD: [RegexHandler('^[0-9]*$', scihub_retrive, pass_user_data=True)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

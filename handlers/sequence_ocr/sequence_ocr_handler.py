from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from . import ocr
import time
PHOTO_OCR = range(1)


def sequence_ocr(bot, update):
    update.message.reply_text('To make recognition, i need photo of sequence. \n Please, send it to me.\n Practices for good recognition: \n - use flash; \n - crop photo to zone you need to recognize; \n try to avoid blur on photos. ')       
    return PHOTO_OCR


def photo_ocr(bot, update):
    user = update.message.from_user
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    update.message.reply_text('Cool! Now, please wait. \n I need some time to read this stuff.')
    start = time.time()
    recognised_string = str(ocr.sequence_ocr_processing(photo_file.file_path)).replace("\n","").upper()
    end = start - time.time()
    update.message.reply_text('Operation tooked: %f seconds. \n Here your sequence: \n %s' % (end, recognised_string))
    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Sorry if i made something wrong( \n However, if you think it\'s bug, or you have idea how to make me better, write to my creator: @dantistnfs')
    return ConversationHandler.END


ocr_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('ocr_sequence', sequence_ocr)],

    states={
        PHOTO_OCR: [MessageHandler(Filters.photo, photo_ocr)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

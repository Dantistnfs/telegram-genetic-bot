from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from . import ocr
PHOTO_OCR = range(1)


def sequence_ocr(bot, update):
    update.message.reply_text('To make recognition, i need photo of sequence. \n Please, send it to me.\n Practices for good recognition: \n - use flash; \n - crop photo to zone you need to recognize; \n try to avoid blur on photos. ')       
    return PHOTO_OCR


def photo_ocr(bot, update):
    user = update.message.from_user
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    update.message.reply_text('Cool! Now, please wait. \n I need some time to read this stuff.')
    download, end, recognised_string = ocr.sequence_ocr_processing(photo_file.file_path)
    update.message.reply_text('Download time: %f sec. \n Operation tooked: %f sec. \n Here your sequence:')
    update.message.reply_text(recognised_string)
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

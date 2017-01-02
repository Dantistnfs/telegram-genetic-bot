from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, RegexHandler)
from . import ocr
try:
    import Image
except ImportError:
    from PIL import Image
import requests
from io import BytesIO, StringIO

DETECTING_PHOTO_BLOCKS, BLOCK_OCR = range(2)

def sequence_ocr(bot, update):
    update.message.reply_text('To make recognition, i need photo of sequence. \n Please, send it to me.\n Practices for good recognition: \n - text should be horizontal; \n - use flash; \n - try to avoid blur on photos. ')       
    return DETECTING_PHOTO_BLOCKS


def detecting_photo_blocks(bot, update, user_data):
    user = update.message.from_user
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    update.message.reply_text('Cool! Now, please wait. \n I need some time to read this stuff.')
    nr_objects, end, image_processed, blocks, image_downloaded = ocr.sequence_ocr_processing(photo_file.file_path)
    update.message.reply_text('Hey, i found %d blocks of text. \n It tooked me %f seconds. \n Please, write me number of block you want to scan with: \n \"[number]\"' % (nr_objects, end))
    image_temp_IO = BytesIO()
    image_processed.save(image_temp_IO, format='png')
    image_temp_IO.seek(0)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=image_temp_IO)
    user_data['image'] = image_downloaded
    user_data['blocks_coordinates'] = blocks
    return BLOCK_OCR

def block_ocr(bot, update, user_data):
    choosed_block = int(update.message.text)
    user = update.message.from_user
    image = user_data['image']
    blocks = user_data['blocks_coordinates']
    choosed_block = blocks[choosed_block]
    image = image.crop((choosed_block[2],choosed_block[0],choosed_block[3],choosed_block[1]))
    recognised_string, time_taked = ocr.ocr_process(image)
    update.message.reply_text('OCR tooked %f seconds.' % time_taked)
    update.message.reply_text(recognised_string)
    update.message.reply_text('Sorry if something wrong, I forgot to wear my googles today.')
    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Sorry if I made something wrong( \n However, if you think it\'s bug, or you have idea how to make me better, write to my creator: @dantistnfs')
    return ConversationHandler.END


ocr_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('ocr_sequence', sequence_ocr)],

    states={
        DETECTING_PHOTO_BLOCKS: [MessageHandler(Filters.photo, detecting_photo_blocks, pass_user_data=True)],
        BLOCK_OCR: [RegexHandler('^[0-9]*$', block_ocr, pass_user_data=True)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

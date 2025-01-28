from telegram import Bot
from telegram.ext import Updater, CommandHandler

# استبدل TOKEN الخاص بك
TOKEN = '1922426592:AAE9Z5qIVVh97Gx8ow2gE8zxyd7CD1GIG2M'

def start(update, context):
    update.message.reply_text('مرحبًا! البوت يعمل.')

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # إضافة معالج للأمر '/start'
    dispatcher.add_handler(CommandHandler('start', start))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
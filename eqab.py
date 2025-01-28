from telegram import Bot
from telegram.ext import Updater, CommandHandler

API_TOKEN = '1922426592:AAE9Z5qIVVh97Gx8ow2gE8zxyd7CD1GIG2M'

# دالة لبدء المحادثة مع البوت
def start(update, context):
    update.message.reply_text("مرحباً! تم اختبار الكود بنجاح!")

def main():
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # إضافة معالج للأوامر
    dispatcher.add_handler(CommandHandler("start", start))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
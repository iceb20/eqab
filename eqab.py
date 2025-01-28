from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ضع التوكن هنا
API_TOKEN = '1922426592:AAE9Z5qIVVh97Gx8ow2gE8zxyd7CD1GIG2M'

# دالة الرد على الأمر /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("مرحباً! تم اختبار الكود بنجاح!")

def main():
    # إنشاء الـ Updater باستخدام الـ Token
    updater = Updater(API_TOKEN)

    # الحصول على الـ Dispatcher
    dispatcher = updater.dispatcher

    # إضافة Handler للأمر /start
    dispatcher.add_handler(CommandHandler("start", start))

    # بدء البوت
    updater.start_polling()

    # استمر في العمل حتى يتم إيقاف البوت
    updater.idle()

if __name__ == '__main__':
    main()
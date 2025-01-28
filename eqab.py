from telegram import Bot
from telegram.ext import Application, CommandHandler

# استبدل TOKEN الخاص بك
TOKEN = '1922426592:AAE9Z5qIVVh97Gx8ow2gE8zxyd7CD1GIG2M'

async def start(update, context):
    await update.message.reply_text('مرحبًا! البوت يعمل.')

def main():
    application = Application.builder().token(TOKEN).build()

    # إضافة معالج للأمر '/start'
    application.add_handler(CommandHandler('start', start))

    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()
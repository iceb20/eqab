from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode

API_TOKEN = '1922426592:AAE9Z5qIVVh97Gx8ow2gE8zxyd7CD1GIG2M'

# إعداد البوت مع تمكين الـ ParseMode
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)  # يمكنك استخدام MarkdownV2 إذا كنت تفضل ذلك
dp = Dispatcher()

@dp.message()
async def echo(message: Message):
    # الرد على الرسائل بنفس التنسيق
    await message.answer(f"<b>Echo:</b> {message.text}")

if __name__ == "__main__":
    dp.run_polling(bot)
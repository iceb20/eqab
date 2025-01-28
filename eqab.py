from aiogram import Bot, Dispatcher, types
import logging
import random
import time
import string

API_TOKEN = '1922426592:AAE9Z5qIVVh97Gx8ow2gE8zxyd7CD1GIG2M'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

user_data = {}
leaderboard = {}
active_codes = {}
banned_users = {}

# لوحة التحكم (أدمن)
admin_user_id = 1109938951

# الأسئلة الصعبة والمتدرجة
questions = [
    {"question": "ما هو الرقم الذري للأوكسجين؟", "answer": "8", "difficulty": 1},
    {"question": "من هو مؤسس شركة مايكروسوفت؟", "answer": "بيل جيتس", "difficulty": 2},
    {"question": "ما هو أكبر كوكب في نظامنا الشمسي؟", "answer": "المشتري", "difficulty": 2},
    {"question": "ما هو اسم عاصمة اليابان؟", "answer": "طوكيو", "difficulty": 3},
    {"question": "من الذي اخترع الهاتف؟", "answer": "ألكسندر غراهام بيل", "difficulty": 3},
    {"question": "ما هو أكبر حيوان على وجه الأرض؟", "answer": "الحوت الأزرق", "difficulty": 4},
    {"question": "متى تم اختراع الإنترنت؟", "answer": "1983", "difficulty": 4},
    {"question": "من هو أول من وصل إلى القمر؟", "answer": "نيل آرمسترونغ", "difficulty": 5},
    {"question": "ما هو أكبر مصدر للطاقة في الكون؟", "answer": "النجوم", "difficulty": 5},
]

# وظيفة لإنشاء أكواد عشوائية
def generate_code(length=8):
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

# وظيفة للتحقق من صلاحية الكود
def validate_code(code):
    return code in active_codes and active_codes[code]['used'] == False

# إنشاء كود جديد من قبل الأدمن
@dp.message_handler(commands=['create_code'])
async def create_code(message: types.Message):
    if message.from_user.id != admin_user_id:
        await message.reply("❌ هذه الميزة محصورة بالأدمن فقط!")
        return

    await message.reply("🔑 من فضلك، اكتب الكود الذي تود إنشاءه، أو اكتب 'عشوائي' لإنشاء كود عشوائي.")

@dp.message_handler(lambda message: message.text.lower() == "عشوائي" or message.text.startswith("كود:"))
async def generate_admin_code(message: types.Message):
    if message.from_user.id != admin_user_id:
        await message.reply("❌ هذه الميزة محصورة بالأدمن فقط!")
        return

    if message.text.lower() == "عشوائي":
        code = generate_code()
        value = random.randint(10, 100)
        active_codes[code] = {'value': value, 'used': False}
        await message.reply(f"✅ تم إنشاء الكود العشوائي بنجاح! الكود هو: {code} ويحتوي على {value} FPX.")
    elif message.text.startswith("كود:"):
        parts = message.text.split(":")
        if len(parts) != 2:
            await message.reply("❌ صيغة الكود غير صحيحة. الرجاء استخدام الصيغة 'كود:<قيمة FPX>'.")
            return
        try:
            value = int(parts[1])
            code = generate_code()
            active_codes[code] = {'value': value, 'used': False}
            await message.reply(f"✅ تم إنشاء الكود بنجاح! الكود هو: {code} ويحتوي على {value} FPX.")
        except ValueError:
            await message.reply("❌ الرجاء إدخال قيمة صحيحة لـ FPX.")

@dp.message_handler(commands=['redeem_code'])
async def redeem_code(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"wallet": 0, "bet": 0, "last_played": time.time(), "wheel_used_today": False, "attempts": 0, "time_left": 0}

    if len(message.text.split()) < 2:
        await message.reply("❌ من فضلك، أدخل الكود بعد الأمر /redeem_code.")
        return

    code = message.text.split()[1].upper()

    if validate_code(code):
        value = active_codes[code]['value']
        user_data[user_id]["wallet"] += value
        active_codes[code]['used'] = True
        await message.reply(f"✅ تم استلام {value} FPX بنجاح! الكود {code} تم استخدامه.")
    else:
        banned_users[user_id] = time.time()
        await message.reply("❌ لقد حاولت استخدام كود غير صالح. تم حظرك لمدة 24 ساعة.")

@dp.message_handler(commands=['spin_wheel'])
async def spin_wheel(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"wallet": 0, "bet": 0, "last_played": time.time(), "wheel_used_today": False, "attempts": 0, "time_left": 0}

    if user_data[user_id]["wheel_used_today"]:
        await message.reply("❌ لقد استخدمت عجلة الحظ اليوم بالفعل. حاول غدًا.")
        return

    user_data[user_id]["wheel_used_today"] = True

    wheel_prizes = ["100 FPX", "كود آيباد بلس", "كود آيفون", "1 FPX", "1 FPX", "1 FPX"]
    prize = random.choice(wheel_prizes)
    if prize == "100 FPX":
        user_data[user_id]["wallet"] += 100
    await message.reply(f"🎉 تم تدوير العجلة! فزت بـ: {prize}")

@dp.message_handler(commands=['ban_user'])
async def ban_user(message: types.Message):
    if message.from_user.id != admin_user_id:
        await message.reply("❌ هذه الميزة محصورة بالأدمن فقط!")
        return

    parts = message.text.split()
    if len(parts) != 2:
        await message.reply("❌ الرجاء تحديد الـ ID الخاص باللاعب الذي تريد حظره.")
        return

    user_id = int(parts[1])
    banned_users[user_id] = time.time()
    await message.reply(f"✅ تم حظر اللاعب ID: {user_id} لمدة 24 ساعة.")

@dp.message_handler(commands=['unban_user'])
async def unban_user(message: types.Message):
    if message.from_user.id != admin_user_id:
        await message.reply("❌ هذه الميزة محصورة بالأدمن فقط!")
        return

    parts = message.text.split()
    if len(parts) != 2:
        await message.reply("❌ الرجاء تحديد الـ ID الخاص باللاعب الذي تريد رفع الحظر عنه.")
        return

    user_id = int(parts[1])
    if user_id in banned_users:
        del banned_users[user_id]
        await message.reply(f"✅ تم رفع الحظر عن اللاعب ID: {user_id}.")
    else:
        await message.reply("❌ اللاعب غير محظور.")

@dp.message_handler()
async def check_ban(message: types.Message):
    user_id = message.from_user.id
    if user_id in banned_users and time.time() - banned_users[user_id] < 86400:
        await message.reply("❌ تم حظر حسابك لمدة 24 ساعة بسبب محاولة استخدام كود غير صالح.")
        return
    elif user_id in banned_users and time.time() - banned_users[user_id] >= 86400:
        del banned_users[user_id]  # رفع الحظر بعد 24 ساعة

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
    
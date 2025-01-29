import telebot
from telebot import types
import requests
import time
import threading

# Telegram Bot API Token
API_TOKEN = '1922426592:AAE9Z5qIVVh97Gx8ow2gE8zxyd7CD1GIG2M'
bot = telebot.TeleBot(API_TOKEN)

# Function to validate session
def validate_session(session_id):
    url = "https://i.instagram.com/api/v1/accounts/current_user/"
    headers = {
        "User-Agent": "Instagram 284.0.0.22.85 Android",
        "Cookie": f"sessionid={session_id}"
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200 and '"status":"ok"' in response.text

# Function to change username
def change_username(session_id, new_username):
    url = "https://i.instagram.com/api/v1/accounts/edit_profile/"
    headers = {
        "User-Agent": "Instagram 284.0.0.22.85 Android",
        "Cookie": f"sessionid={session_id}"
    }
    data = {"username": new_username}
    response = requests.post(url, headers=headers, data=data)
    return response.status_code == 200 and '"status":"ok"' in response.text

# Function to perform Swap
def perform_swap(message, main_session, target_session, username):
    if not validate_session(main_session) or not validate_session(target_session):
        bot.send_message(message.chat.id, "❌ One of the sessions is invalid. Check and try again.")
        return

    temp_username = f"{username}_tmp_{int(time.time())}"
    change_username(main_session, temp_username)

    success = False
    attempts = 0
    while not success and attempts < 10:
        success = change_username(target_session, username)
        attempts += 1
        time.sleep(0.2)

    if success:
        bot.send_message(message.chat.id, "✅ Username transferred successfully!")
    else:
        bot.send_message(message.chat.id, "❌ Transfer failed. Someone else might have taken the username.")

# Function to bypass 14-day restriction
def bypass_14_days(message, session_id, username):
    url = "https://i.instagram.com/api/v1/accounts/set_username/"
    headers = {
        "User-Agent": "Instagram 284.0.0.22.85 Android",
        "Cookie": f"sessionid={session_id}"
    }
    data = {"username": username}
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200 and '"status":"ok"' in response.text:
        bot.send_message(message.chat.id, "✅ 14-Day restriction bypassed successfully!")
    else:
        bot.send_message(message.chat.id, "❌ Failed to bypass 14-day restriction. Try again later.")

# Function to auto-reclaim username
def auto_reclaim(message, main_session, backup_session, username):
    success = change_username(main_session, username)

    if not success:
        success = change_username(backup_session, username)

    if success:
        bot.send_message(message.chat.id, "✅ Username auto-reclaimed successfully!")
    else:
        bot.send_message(message.chat.id, "❌ Failed to auto-reclaim the username.")

# Function to change Bio
def change_bio(message, session_id, new_bio):
    url = "https://i.instagram.com/api/v1/accounts/edit_profile/"
    headers = {
        "User-Agent": "Instagram 284.0.0.22.85 Android",
        "Cookie": f"sessionid={session_id}"
    }
    data = {"biography": new_bio}
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        bot.send_message(message.chat.id, "✅ Bio changed successfully!")
    else:
        bot.send_message(message.chat.id, "❌ Failed to change bio.")

# Telegram Bot Handlers
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Swap')
    item2 = types.KeyboardButton('Bypass')
    item3 = types.KeyboardButton('Settings')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "🔥 Welcome to EqAb Tool 🔥", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Swap')
def handle_swap(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Run Swap', 'Close Swap', 'Set Main Session', 'Set Target Session', 'Check Block', 'Threads Swap', 'Back')
    bot.send_message(message.chat.id, "Select Swap Mode", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Bypass')
def handle_bypass(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Run Bypass', 'Close Bypass', 'Set Auto Sessions', 'Set Threads Auto', 'Set Bypass Session', 'R/s release', 'Back')
    bot.send_message(message.chat.id, "Select Bypass Mode", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Settings')
def handle_settings(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Proxy Bypass', 'Gif', 'Webhook', 'Swap', 'Proxy Swap', 'Name', 'Bio', 'Webhook', 'Bypass', 'Auto Releaser', 'Back')
    bot.send_message(message.chat.id, "Select Settings Mode", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Run Swap')
def handle_run_swap(message):
    bot.send_message(message.chat.id, "⚡ Enter main session ID:")
    bot.register_next_step_handler(message, get_main_session)

def get_main_session(message):
    main_session = message.text
    bot.send_message(message.chat.id, "⚡ Enter target session ID:")
    bot.register_next_step_handler(message, get_target_session, main_session)

def get_target_session(message, main_session):
    target_session = message.text
    bot.send_message(message.chat.id, "⚡ Enter the username to swap:")
    bot.register_next_step_handler(message, execute_swap, main_session, target_session)

def execute_swap(message, main_session, target_session):
    username = message.text
    threading.Thread(target=perform_swap, args=(message, main_session, target_session, username)).start()

@bot.message_handler(func=lambda message: message.text == 'Run Bypass')
def handle_run_bypass(message):
    bot.send_message(message.chat.id, "⚡ Enter session ID:")
    bot.register_next_step_handler(message, get_bypass_session)

def get_bypass_session(message):
    session_id = message.text
    bot.send_message(message.chat.id, "⚡ Enter username to bypass:")
    bot.register_next_step_handler(message, execute_bypass, session_id)

def execute_bypass(message, session_id):
    username = message.text
    threading.Thread(target=bypass_14_days, args=(message, session_id, username)).start()

@bot.message_handler(func=lambda message: message.text == 'Bio')
def handle_bio_change(message):
    bot.send_message(message.chat.id, "⚡ Enter session ID:")
    bot.register_next_step_handler(message, get_bio_session)

def get_bio_session(message):
    session_id = message.text
    bot.send_message(message.chat.id, "⚡ Enter new bio text:")
    bot.register_next_step_handler(message, execute_bio_change, session_id)

def execute_bio_change(message, session_id):
    new_bio = message.text
    threading.Thread(target=change_bio, args=(message, session_id, new_bio)).start()

# Start bot polling
bot.polling(none_stop=True)
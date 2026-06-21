import telebot
from telebot import types
import requests

# 1. ያንተ ቶክን
BOT_TOKEN = "8376770759:AAHo__-Ih_6CpkJtpUhXbuKQ3EhKH7JYNBs"
bot = telebot.TeleBot(BOT_TOKEN)

# ለተጠቃሚዎች ምርጫ መያዣ
user_status = {}

# 2. የሶሻል ሚዲያ መምረጫ ሜኑ
def get_platform_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔹 Telegram", callback_data="check_telegram"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="check_instagram"),
        types.InlineKeyboardButton("🎵 TikTok", callback_data="check_tiktok"),
        types.InlineKeyboardButton("🐦 Twitter", callback_data="check_twitter")
    )
    return markup

# 3. /start
@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.send_message(
        message.chat.id,
        "👋 እንኳን ወደ አካውንት ቼከር ቦት በደህና መጡ!\n\nምርጫዎን ይምረጡ:",
        reply_markup=get_platform_menu()
    )

# 4. ምርጫ መቀበያ
@bot.callback_query_handler(func=lambda call: call.data.startswith("check_"))
def callback_handler(call):
    platform = call.data.split("_")[1]
    user_status[call.message.chat.id] = platform
    bot.edit_message_text(
        f"✅ {platform.upper()} ተመርጧል።\nእባክዎ ዩዘርኔሙን ይላኩ (ምሳሌ: @ak)",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )

# 5. ዩዘርኔም ቼክ ማድረጊያ
@bot.message_handler(func=lambda m: m.chat.id in user_status and user_status[m.chat.id] is not None)
def check_logic(message):
    platform = user_status[message.chat.id]
    username = message.text.replace("@", "").strip()
    
    url = f"https://t.me/{username}" if platform == "telegram" else f"https://{platform}.com/{username}"
    
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            msg = f"✅ አካውንቱ አለ! \n🔗 ሊንክ: {url}"
        else:
            msg = "❌ Query failed: አካውንቱ የለም።"
    except:
        msg = "⚠️ Network error."
        
    bot.send_message(message.chat.id, msg)
    user_status[message.chat.id] = None # ማጽዳት

bot.infinity_polling()

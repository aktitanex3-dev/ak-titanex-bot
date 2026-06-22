import telebot
from telebot import types
from flask import Flask
import threading

# 1. መሠረታዊ ነገሮች
TOKEN = "8376770759:AAHo__-Ih_6CpkJtpUhXbuKQ3EhKH7JYNBs"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Render ላይ ቦቱ እንዲነቃ የሚያደርግ Flask አፕ
@app.route('/')
def home(): return "Bot is running!"

def keep_alive():
    app.run(host="0.0.0.0", port=8080)

# የተጠቃሚ መረጃ (State)
user_data = {}

# --- ዋናው ሜኑ ---
def get_main_menu(lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # አማርኛ/እንግሊዝኛ ጽሑፎች
    texts = {
        "am": ["🌐 Website", "🤖 Bot", "📱 App", "📈 Management", "📣 Promotion", "🔄 Resell", "ℹ️ ስለ እኛ", "📝 አስተያየት"],
        "en": ["🌐 Website", "🤖 Bot", "📱 App", "📈 Management", "📣 Promotion", "🔄 Resell", "ℹ️ About Us", "📝 Feedback"]
    }
    t = texts[lang]
    markup.add(
        types.InlineKeyboardButton(t[0], callback_data="serv_web"),
        types.InlineKeyboardButton(t[1], callback_data="serv_bot"),
        types.InlineKeyboardButton(t[2], callback_data="serv_app"),
        types.InlineKeyboardButton(t[3], callback_data="serv_manage"),
        types.InlineKeyboardButton(t[4], callback_data="serv_promo"),
        types.InlineKeyboardButton(t[5], callback_data="serv_resell"),
        types.InlineKeyboardButton(t[6], callback_data="about"),
        types.InlineKeyboardButton(t[7], callback_data="feedback")
    )
    return markup

# --- የቋንቋ ምርጫ ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("አማርኛ", callback_data="lang_am"),
               types.InlineKeyboardButton("English", callback_data="lang_en"))
    bot.send_message(message.chat.id, "እንኳን ደህና መጡ! ቋንቋ ይምረጡ.\nWelcome! Please choose a language.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    
    # ቋንቋ መምረጥ
    if call.data.startswith("lang_"):
        lang = call.data.split("_")[1]
        user_data[chat_id] = {'lang': lang}
        msg = "እባክዎ የሚፈልጉትን አገልግሎት ይምረጡ:" if lang == "am" else "Please select the service you need:"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_main_menu(lang))
    
    # ወደ ዋናው ሜኑ መመለስ
    elif call.data == "back_main":
        lang = user_data.get(chat_id, {}).get('lang', 'am')
        msg = "አገልግሎት ይምረጡ:" if lang == "am" else "Select a service:"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_main_menu(lang))

# --- ቦቱን ማስነሻ ---
if __name__ == "__main__":
    # Flask ሰርቨሩን በተለየ Thread ማስጀመር
    threading.Thread(target=keep_alive).start()
    bot.infinity_polling()

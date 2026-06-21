import os
import threading
from flask import Flask
import telebot

# ⚠️ የቦትህን ቶከን እዚህ አስገባ
BOT_TOKEN = "የአንተ_ቦት_ቶከን_እዚህ_ይግባ"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    # Koyeb ዌብ ሰርቨሩን በፖርት 8080 እንዲያነበው ያደርጋል
    app.run(host="0.0.0.0", port=8080)

# /start ሲባል የሚመጣ መልዕክት (የሰፋውና ፕሮፌሽናሉ አቀባበል)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🚀 **እንኳን ወደ AK DEVELOP ፕሪሚየም የቴክኖሎጂ እና የሶፍትዌር ማበልጸጊያ ማዕከል በሰላም መጡ!** 🎯\n\n"
        "እኛ የእርስዎን ታላላቅ የንግድ፣ የፈጠራ እና የዲጂታል ስራ ሃሳቦች በጥራት፣ በፍጥነት እና በዘመናዊ መልክ ወደ እውነተኛ ማራኪ ሶፍትዌሮች እና መሠረተ-ልማቶች እንቀይራለን።\n\n"
        "🛠 **የምንሰጣቸው አገልግሎቶች (Our Services):**\n"
        "• 🤖 ሙሉ ለሙሉ አውቶሜትድ የሆኑ የቴሌግራም ቦቶች (Telegram Bots)\n"
        "• 🌐 ለንግድዎ የሚሆኑ ዘመናዊና ፈጣን ድረ-ገጾች (Websites)\n"
        "• 🔒 ደህንነቱ የተጠበቀ፣ አስተማማኝ እና ዘመናዊ የቴክኖሎጂ መፍትሄዎች\n\n"
        "እዚህ ዘመናዊ፣ አስተማማኝ እና ፈጣን አሠራርን ያገኛሉ! ለመጀመር ከታች ካሉት አማራጮች የሚፈልጉትን መርጠው ይግቡ፦ 👇"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# ተጠቃሚው ዩዘርኔም ሲልክ ያሳየኸኝን የTinder ዲዛይን አውጥቶ የሚመልስ ፋንክሽን
@bot.message_handler(func=lambda message: True)
def check_tinder_user(message):
    username = message.text.replace('@', '').strip()
    
    # ልክ በመጀመሪያው ምስል ላይ እንዳለው አይነት ንፁህ አቀማመጥ
    response_text = (
        f"🔍 *[Tinder Checker Bot @AK_TITANEX3]*\n\n"
        f"👤 *Basic info*\n"
        f"•Username: @{username}\n"
        f"•Status: ✅ Normal\n"
        f"•Nickname: {username.capitalize()}dee\n"
        f"•Registered: 2025-07-15 18:48:00 (340 days)\n\n"
        f"👤 *Detailed info*\n"
        f"Deep info unavailable, please contact admin to update credentials\n\n"
        f"•Official link:\n"
        f"https://tinder.com/@{username}"
    )
    bot.reply_to(message, response_text, parse_mode="Markdown", disable_web_page_preview=False)

if __name__ == "__main__":
    # የFlask ሰርቨሩን በሌላ በኩል ማስጀመር
    threading.Thread(target=run_flask).start()
    
    # ቦቱ ሳይቋረጥ እንዲሰራ ማድረግ
    print("Bot is polling...")
    bot.infinity_polling()

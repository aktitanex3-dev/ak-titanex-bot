@bot.message_handler(commands=['start'])
def start(message):
    # የቋንቋ ምርጫ በተኖች
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("አማርኛ 🇪🇹", callback_data="lang_am"),
               types.InlineKeyboardButton("English 🇺🇸", callback_data="lang_en"))
    
    # 5 መስመር ያለው የሰላምታ መልእክት (Bilingual)
    start_text = (
        "🌟 *AK DEVELOP ORDER CENTER* 🌟\n"
        "- 🚀 የእርስዎ የዲጂታል አገልግሎት ማዕከል! / Your digital service hub!\n"
        "- 🌐 ጥራት ያለው የዌብሳይትና የቦት ስራዎች! / Quality Website & Bot services!\n"
        "- ⚡ ፈጣን እና አስተማማኝ ድጋፍ እንሰጣለን! / Fast & reliable support!\n"
        "- 👇 እባክዎን ቋንቋ ይምረጡ / Please choose a language:"
    )
    
    bot.send_message(message.chat.id, start_text, parse_mode="Markdown", reply_markup=markup)

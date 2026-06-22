# --- የሜኑ ፋንክሽኖች (እነዚህን ከላይ አስቀምጣቸው) ---
def get_main_menu(lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    texts = {
        "am": ["🌐 ዌብሳይት", "🤖 ቦት", "📱 አፕ", "📈 ማኔጅመንት", "📣 ፕሮሞሽን", "🔄 ሪሰል", "ℹ️ ስለ እኛ", "📝 አስተያየት"],
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

def get_website_menu(lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    types_am = ["ኢ-ኮሜርስ", "ፖርትፎሊዮ", "ብሎግ", "ኩባንያ", "ሌላ (Other)"]
    types_en = ["E-commerce", "Portfolio", "Blog", "Business", "Other"]
    t = types_am if lang == "am" else types_en
    for i, name in enumerate(t):
        markup.add(types.InlineKeyboardButton(name, callback_data=f"web_type_{i}"))
    markup.add(types.InlineKeyboardButton("🔙 ተመለስ / Back", callback_data="back_main"))
    return markup

# --- የተዋሃደው የCallback Handler ---
@bot.callback_query_handler(func=lambda call: True)
def all_callbacks(call):
    chat_id = call.message.chat.id
    lang = user_data.get(chat_id, {}).get('lang', 'am')

    # 1. የቋንቋ ምርጫ
    if call.data.startswith("lang_"):
        lang = call.data.split("_")[1]
        user_data[chat_id] = {'lang': lang}
        msg = "እባክዎ የሚፈልጉትን አገልግሎት ይምረጡ:" if lang == "am" else "Please select a service:"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_main_menu(lang))
    
    # 2. ወደ ዋናው ሜኑ መመለስ
    elif call.data == "back_main":
        bot.edit_message_text("አገልግሎት ይምረጡ:" if lang == "am" else "Select a service:", chat_id, call.message.message_id, reply_markup=get_main_menu(lang))
    
    # 3. የዌብሳይት ሜኑ መክፈቻ
    elif call.data == "serv_web":
        bot.edit_message_text("የዌብሳይት ዓይነት ይምረጡ:" if lang == "am" else "Select website type:", chat_id, call.message.message_id, reply_markup=get_website_menu(lang))
    
    # 4. የዌብሳይት ዓይነት ሲመረጥ
    elif call.data.startswith("web_type_"):
        user_data[chat_id]['selected_web'] = call.data
        msg = "ይህንን ነው የሚፈልጉት? (አዎ/አይ)" if lang == "am" else "Is this what you want? (Yes/No)"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ አዎ / Yes", callback_data="web_confirm_yes"),
                   types.InlineKeyboardButton("❌ አይ / No", callback_data="serv_web"))
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=markup)

    # 5. ሲረጋገጥ (ጥያቄዎች ሲጀምሩ)
    elif call.data == "web_confirm_yes":
        user_data[chat_id]['state'] = 'web_q1'
        user_data[chat_id]['answers'] = []
        q = "1. ዌብሳይቱ እንዴት እንደሚሰራ ይግለጹ:" if lang == "am" else "1. Explain how the website works:"
        bot.edit_message_text(q, chat_id, call.message.message_id)

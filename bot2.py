import logging
import os
import requests  # Fayllarni yuklab olish uchun kerak
from io import BytesIO # Faylni xotirada ushlab turish uchun
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from flask import Flask
from threading import Thread

# --- 1-QISM: WEB SERVER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "EKO 27 Bot is active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2-QISM: TELEGRAM BOT ---

BOT_TOKEN = "7447417490:AAFSte68lEYPtxNC2WJysMS__LtrgFibhOc"

# To'g'ridan-to'g'ri fayl manzillari
APK_URL = "https://github.com/abdurazoqov606/Appp/raw/refs/heads/main/abbos-debug.apk"
IMG_URL = "https://github.com/abdurazoqov606/Appp/raw/refs/heads/main/IMG_20260211_120023.jpg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    text = (
        f"Assalomu alaykum, {user_first_name}! 👋\n\n"
        f"Xush kelibsiz! 🌱 **EKO 27** loyihasiga qo'shiling.\n\n"
        f"👤 **Loyiha asoschisi:** Abdurazoqov Abbos (@vsf911)\n"
    )
    
    inline_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Saytga Kirish", url="https://loyiha27w.vercel.app/")]])
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("📥 Loyiha ilovasini yuklab olish")]], resize_keyboard=True)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ilovani yuklab olish uchun tugmani bosing:", reply_markup=inline_markup)

async def send_app_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    processing_msg = await update.message.reply_text("⏳ Fayllar tayyorlanmoqda, iltimos kuting...")

    try:
        # 1. Rasmni yuklab olish va yuborish
        response_img = requests.get(IMG_URL)
        if response_img.status_code == 200:
            await context.bot.send_photo(chat_id=chat_id, photo=BytesIO(response_img.content))
        
        caption_text = (
            "✅ **Ilova xavfsiz!**\n"
            "Siz uchun muammo tugʻdirmaydi, maxfiylik mavjud.\n\n"
            "🌿 **EKO 27 jamoasi sizni qoʻllab-quvvatlaydi.**"
        )
        await context.bot.send_message(chat_id=chat_id, text=caption_text, parse_mode='Markdown')

        # 2. APKni yuklab olish va yuborish
        response_apk = requests.get(APK_URL)
        if response_apk.status_code == 200:
            await context.bot.send_document(
                chat_id=chat_id,
                document=BytesIO(response_apk.content),
                filename="EKO_27.apk",
                caption="📱 EKO 27 - Android Ilova"
            )
        else:
            await update.message.reply_text("❌ Faylni yuklab olishda xatolik yuz berdi (GitHub xatosi).")

        await context.bot.delete_message(chat_id=chat_id, message_id=processing_msg.message_id)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Texnik xatolik: {e}")

if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Regex("^📥 Loyiha ilovasini yuklab olish$"), send_app_files))
    
    print("EKO 27 boti ishlamoqda...")
    application.run_polling()

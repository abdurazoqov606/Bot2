import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from flask import Flask
from threading import Thread

# --- 1-QISM: WEB SERVER (Render/Replit da 24/7 ishlash uchun) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "EKO 27 Bot is active and running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2-QISM: TELEGRAM BOT SOZLAMALARI ---

# Bot Tokeningiz
BOT_TOKEN = "7447417490:AAFSte68lEYPtxNC2WJysMS__LtrgFibhOc"

# Havolalar (Siz bergan aniq manzillar)
APK_URL = "https://github.com/abdurazoqov606/Appp/raw/refs/heads/main/abbos-debug.apk"
IMG_URL = "https://github.com/abdurazoqov606/Appp/raw/refs/heads/main/IMG_20260211_120023.jpg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    
    text = (
        f"Assalomu alaykum, {user_first_name}! 👋\n\n"
        f"Xush kelibsiz! 🌱\n"
        f"Bizning **EKO 27** loyihamizda ishtirok eting.\n\n"
        f"👤 **Loyiha asoschisi:** Abdurazoqov Abbos (@vsf911)\n\n"
        f"👇 Quyidagi menyudan kerakli bo'limni tanlang:"
    )

    # Saytga o'tish tugmasi (Xabar tagida)
    inline_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Loyiha Saytiga Kirish", url="https://loyiha27w.vercel.app/")]
    ])

    # Pastki menyu tugmasi (Klaviaturada)
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("📥 Loyiha ilovasini yuklab olish")]],
        resize_keyboard=True
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode='Markdown',
        reply_markup=inline_markup
    )
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📲 Ilovani yuklab olish uchun pastdagi tugmani bosing:",
        reply_markup=reply_markup
    )

async def send_app_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # 1. Yuklanayotgani haqida xabar berish
    processing_msg = await update.message.reply_text("⏳ Ilova serverdan yuklanmoqda, ozgina kuting...")

    try:
        caption_text = (
            "✅ **Ilova xavfsiz!**\n"
            "Siz uchun muammo tugʻdirmaydi, maxfiylik mavjud.\n\n"
            "🌿 **EKO 27 jamoasi sizni qoʻllab-quvvatlaydi.**"
        )

        # 2. Rasmni yuborish
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=IMG_URL
        )

        # 3. Matnni yuborish
        await context.bot.send_message(
            chat_id=chat_id,
            text=caption_text,
            parse_mode='Markdown'
        )

        # 4. APK faylni yuborish
        # read_timeout va write_timeout fayl katta bo'lsa uzilib qolmasligi uchun kerak
        await context.bot.send_document(
            chat_id=chat_id,
            document=APK_URL,
            filename="EKO_27.apk",
            caption="📱 EKO 27 - Android Ilova",
            read_timeout=300, 
            write_timeout=300,
            connect_timeout=300
        )
        
        # "Yuklanmoqda" xabarini o'chirish
        await context.bot.delete_message(chat_id=chat_id, message_id=processing_msg.message_id)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    # Web serverni alohida oqimda ishga tushiramiz
    keep_alive()
    
    # Botni ishga tushiramiz
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlerlar
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Regex("^📥 Loyiha ilovasini yuklab olish$"), send_app_files))
    
    print("Bot EKO 27 muvaffaqiyatli ishga tushdi...")
    application.run_polling()
    

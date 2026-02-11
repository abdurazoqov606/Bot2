import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from flask import Flask
from threading import Thread

# --- 1-QISM: WEB SERVER (Renderda 24/7 ishlash uchun) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "EKO 27 Bot is running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2-QISM: TELEGRAM BOT LOGIKASI ---

# Token
BOT_TOKEN = "7447417490:AAFSte68lEYPtxNC2WJysMS__LtrgFibhOc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    
    # 1. Asosiy Xabar matni
    text = (
        f"Assalomu alaykum, {user_first_name}! 👋\n\n"
        f"Xush kelibsiz! 🌱\n"
        f"Bizning **EKO 27** loyihamizda ishtirok eting va kelajakka hissa qo'shing.\n\n"
        f"👤 **Loyiha asoschisi:** Abdurazoqov Abbos (@vsf911)\n\n"
        f"👇 Quyidagi menyudan kerakli bo'limni tanlang:"
    )

    # 2. Saytga o'tish tugmasi (Xabar tagida chiqadi)
    inline_keyboard = [
        [InlineKeyboardButton("🌐 Loyiha Saytiga Kirish", url="https://loyiha27w.vercel.app/")]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    # 3. Pastki Menyu tugmasi (Klaviaturada chiqadi)
    reply_keyboard = [
        [KeyboardButton("📥 Loyiha ilovasini yuklab olish")]
    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)

    # Xabarni yuborish (Sayt tugmasi bilan)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode='Markdown',
        reply_markup=inline_markup
    )
    
    # Pastki menyuni chiqarish uchun qo'shimcha kichik xabar
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📲 Ilovani yuklab olish uchun pastdagi tugmani bosing:",
        reply_markup=reply_markup
    )

async def send_app_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Foydalanuvchiga "Yuklanmoqda..." deb xabar berib turish (ixtiyoriy, lekin foydali)
    processing_msg = await update.message.reply_text("⏳ Ma'lumotlar yuklanmoqda, iltimos kuting...")

    try:
        # GitHub RAW havolalari (To'g'ridan-to'g'ri faylga eltadi)
        img_url = "https://github.com/abdurazoqov606/Appp/raw/main/IMG_20260211_120023.jpg"
        apk_url = "https://github.com/abdurazoqov606/Appp/raw/main/abbos-debug.apk"
        
        caption_text = (
            "✅ **Ilova xavfsiz!**\n"
            "Siz uchun muammo tugʻdirmaydi, maxfiylik mavjud.\n\n"
            "🌿 **EKO 27 jamoasi sizni qoʻllab-quvvatlaydi.**"
        )

        chat_id = update.effective_chat.id

        # 1. Rasmni yuborish
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img_url
        )

        # 2. Matnni yuborish
        await context.bot.send_message(
            chat_id=chat_id,
            text=caption_text,
            parse_mode='Markdown'
        )

        # 3. APK faylni yuborish
        await context.bot.send_document(
            chat_id=chat_id,
            document=apk_url,
            caption="📱 EKO 27 - Android Ilova",
            read_timeout=60, # Katta fayllar uchun vaqtni uzaytiramiz
            write_timeout=60
        )
        
        # "Yuklanmoqda" xabarini o'chirish
        await context.bot.delete_message(chat_id=chat_id, message_id=processing_msg.message_id)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    keep_alive() # Web serverni ishga tushirish
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Start komandasi
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    # "Loyiha ilovasini yuklab olish" tugmasi bosilganda ishlaydigan handler
    # Bu funksiya aynan shu so'z yozilganda ishga tushadi
    app_handler = MessageHandler(filters.Regex("^📥 Loyiha ilovasini yuklab olish$"), send_app_files)
    application.add_handler(app_handler)
    
    print("Bot EKO 27 ishga tushdi...")
    application.run_polling()

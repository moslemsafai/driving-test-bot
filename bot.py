from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import sqlite3
import os

# توکن ربات
TOKEN = "6777321754:AAHeJG9qqU3ZBLmqP2JKU67G-rmBm8-ut2I"

# ایجاد دیتابیس SQLite
def init_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        is_premium INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# بررسی اشتراک ویژه
def check_premium(user_id):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT is_premium FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] == 1 if result else False

# استارت ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()
    
    keyboard = [[InlineKeyboardButton("آزمون‌ها", callback_data="tests")],
                [InlineKeyboardButton("آموزش", callback_data="education")],
                [InlineKeyboardButton("تاریخچه آزمون‌ها", callback_data="history")],
                [InlineKeyboardButton("پاک کردن همه اطلاعات", callback_data="clear")],
                [InlineKeyboardButton("پشتیبانی", callback_data="support")],
                [InlineKeyboardButton("اشتراک ویژه", callback_data="premium")]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("به ربات راهنمایی و رانندگی خوش آمدید!", reply_markup=reply_markup)

# مدیریت دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "support":
        await query.message.reply_text("برای تماس با پشتیبانی با آیدی زیر در ارتباط باشید:\n @Safaimoslem\n\n<b>موفق باشید!</b>", parse_mode="HTML")
    elif query.data == "premium":
        await query.message.reply_text("برای استفاده کامل از ربات و شرکت در بیش از ۲۸ آزمون جامع، اشتراک ویژه را تهیه کنید.\n\n" 
                                      "💰 هزینه فعال‌سازی: ۱۰۰ هزار تومان\n\n" 
                                      "برای فعال‌سازی به آیدی زیر پیام دهید:\n @Safaimoslem", parse_mode="HTML")
    elif query.data == "clear":
        user_id = query.message.chat_id
        conn = sqlite3.connect("bot_data.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        await query.message.reply_text("✅ اطلاعات شما با موفقیت پاک شد!")
    else:
        await query.message.reply_text("🚧 این بخش در حال توسعه است!")

# اجرای ربات
if __name__ == "__main__":
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler

# لیست کاربران دارای اشتراک ویژه
vip_users = set()

def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    text = """
    \U0001F697 *بات آزمون رانندگی*
    
    ✅ امکان استفاده از آموزش‌های داخل ربات و آماده شدن برای آزمون
    ♻️ داشتن بیش از ۲۵ نوع آزمون
    ⚖ محاسبه خودکار درصد قبولی شما
    📅 تاریخچه آزمون‌ها
    ✨ بیشمار قابلیت جذاب دیگر...
    
    موفق باشید!
    """
    keyboard = [
        [InlineKeyboardButton("آموزش", callback_data='education')],
        [InlineKeyboardButton("آزمون‌ها", callback_data='tests')],
        [InlineKeyboardButton("احتمال قبولی", callback_data='probability')],
        [InlineKeyboardButton("تاریخچه آزمون‌ها", callback_data='history')],
        [InlineKeyboardButton("پاک کردن همه اطلاعات", callback_data='clear_data')],
        [InlineKeyboardButton("پشتیبانی", callback_data='support')],
        [InlineKeyboardButton("اشتراک ویژه", callback_data='vip')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown', reply_markup=reply_markup)

def show_tests(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    keyboard = [[InlineKeyboardButton(f"آزمون {i}", callback_data=f'test_{i}') for i in range(1, 6)]]
    keyboard.append([InlineKeyboardButton("بازگشت", callback_data='dashboard')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("لطفاً یک آزمون را انتخاب کنید:", reply_markup=reply_markup)

def start_test(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    test_number = query.data.split('_')[1]
    
    if test_number != "1" and chat_id not in vip_users:
        query.answer("برای انجام این آزمون نیاز به اشتراک ویژه دارید.")
        return
    
    text = f"آزمون {test_number}\nتعداد سوالات: 30\nمدت زمان: 30 دقیقه"
    keyboard = [[InlineKeyboardButton("شروع آزمون", callback_data=f'start_{test_number}')]]
    keyboard.append([InlineKeyboardButton("بازگشت", callback_data='tests')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup)

def handle_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data
    if data == "dashboard":
        start(update, context)
    elif data == "tests":
        show_tests(update, context)
    elif data.startswith("test_"):
        start_test(update, context)
    elif data == "support":
        query.edit_message_text("برای پشتیبانی به آیدی @Safaimoslem پیام دهید.")
    elif data == "vip":
        query.edit_message_text("برای خرید اشتراک ویژه به آیدی @Safaimoslem پیام دهید.")

def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

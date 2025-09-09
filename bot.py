import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
DOWNLOAD_FILE_URL = os.getenv("DOWNLOAD_FILE_URL", "https://example.com/sample.zip")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ℹ️ Info", callback_data="info")],
        [InlineKeyboardButton("📥 Download", callback_data="download")],
        [InlineKeyboardButton("📞 Contact", callback_data="contact")]
    ]
    await update.message.reply_text("👋 Welcome to Sohil Modz Bot!", reply_markup=InlineKeyboardMarkup(keyboard))

# Button handling
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "info":
        keyboard = [[InlineKeyboardButton("🌐 Visit Website", url="https://example.com")]]
        await query.message.reply_text("ℹ️ This is Sohil Modz Bot.\nHere you get files & updates!", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "download":
        await query.message.reply_document(document=DOWNLOAD_FILE_URL, filename="mod_file.zip")

    elif query.data == "contact":
        await query.message.reply_text("📞 Contact Owner: @SohilModz")

# /broadcast (admin only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not authorized!")
        return
    
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: /broadcast <message>")
        return

    await update.message.reply_text("✅ Broadcast sent!")
    # NOTE: User list save karna hoga agar sabko bhejna hai

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()

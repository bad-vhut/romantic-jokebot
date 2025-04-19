import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from dotenv import load_dotenv
import openai
import random

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# কিছু উদাহরণস্বরূপ জোকস ও প্রেমের কবিতা
jokes = [
    "প্রেমিক: আমি তোমার জন্য সব ছাড়তে রাজি আছি। প্রেমিকা: সত্যি? প্রেমিক: হ্যাঁ। প্রেমিকা: তাহলে আমাকে ছেড়ে দাও!",
    "প্রেমিকা: যদি আমাদের বিয়ে হয় তাহলে তুমি সিগারেট ছেড়ে দিবে? প্রেমিক: ওকে। প্রেমিকা: ড্রিংকস করাও না। প্রেমিক: ওকে। প্রেমিকা: নাইট ক্লাবেও যেতে পারবেনা। প্রেমিক: ওকে। প্রেমিকা: আর কি বাকী আছে যা তুমি ছেড়ে দিবে? প্রেমিক: তোমাকে!"
]

love_poems = [
    "তোমার চোখে আমি হারিয়ে যাই, তোমার হাসিতে আমি বাঁচি।",
    "তোমার প্রেমে আমি পাগল, তোমার ভালোবাসায় আমি মুগ্ধ।"
]

love_stories = [
    "এক কাপ কফি: এক সকালে কফি শপে দেখা হলো তাদের, শুরু হলো এক নতুন প্রেমের গল্প।",
    "বৃষ্টিতে ফেরা: বৃষ্টির দিনে পুরনো প্রেমিক-প্রেমিকার হঠাৎ দেখা, আবার জেগে উঠলো পুরনো অনুভূতি।"
]

# AI এর মাধ্যমে জবাব
async def ai_response(message: str) -> str:
    prompt = f"একজন মজার, রোমান্টিক এবং বুদ্ধিমান AI হিসেবে, বাংলা ভাষায় উত্তর দাও:\n\nপ্রশ্ন: {message}\nউত্তর:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("😂 জোকস", callback_data='joke')],
        [InlineKeyboardButton("💖 প্রেমের কবিতা", callback_data='poem')],
        [InlineKeyboardButton("📖 প্রেমের গল্প", callback_data='story')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("হ্যালো! আমি তোমার হাসি-মজা আর প্রেমের গল্পের সাথী। নিচের অপশনগুলো থেকে বেছে নাও:", reply_markup=reply_markup)

# ইনলাইন বাটনের হ্যান্ডলার
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'joke':
        await query.edit_message_text(text=random.choice(jokes))
    elif query.data == 'poem':
        await query.edit_message_text(text=random.choice(love_poems))
    elif query.data == 'story':
        await query.edit_message_text(text=random.choice(love_stories))

# সব ম্যাসেজে জবাব
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = await ai_response(user_message)
    await update.message.reply_text(reply)

# বট চালানো
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

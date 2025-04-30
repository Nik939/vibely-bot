
import os
from flask import Flask, request
import openai
from telegram import Update, Bot, InputFile
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

TOKEN = os.getenv("7750380246:AAHyabZQ_GNJrAqKaqjojAF7tn7KFDpMIGM")
OPENAI_KEY = os.getenv("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")
bot = Bot(token=TOKEN)
openai.api_key = OPENAI_KEY

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет, я Vibely 🤖\n"
        "Генерирую идеи, тексты и образы на креативной скорости.\n"
        "Просто напиши команду:\n"
        "/text пост о кофе\n"
        "/idea идея для стартапа\n"
        "/image летающий кит"
    )

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "/text [запрос] — сгенерировать текст\n"
        "/idea [тема] — идея поста, видео, проекта\n"
        "/image [описание] — сгенерировать картинку"
    )

def generate_text(update: Update, context: CallbackContext):
    prompt = " ".join(context.args)
    if not prompt:
        update.message.reply_text("Напиши что сгенерировать: /text пост о кофе")
        return
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content.strip()
    update.message.reply_text(text)

def generate_idea(update: Update, context: CallbackContext):
    topic = " ".join(context.args)
    if not topic:
        update.message.reply_text("Напиши тему: /idea маркетинг")
        return
    prompt = f"Придумай креативную идею по теме: {topic}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content.strip()
    update.message.reply_text(text)

def generate_image(update: Update, context: CallbackContext):
    prompt = " ".join(context.args)
    if not prompt:
        update.message.reply_text("Напиши описание картинки: /image летающий кит")
        return
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url = response['data'][0]['url']
    update.message.reply_photo(photo=image_url)

dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("text", generate_text))
dispatcher.add_handler(CommandHandler("idea", generate_idea))
dispatcher.add_handler(CommandHandler("image", generate_image))

@app.route("/", methods=["GET"])
def index():
    return "Vibely is running!"

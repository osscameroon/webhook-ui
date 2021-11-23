import time

import requests
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from app.settings import TELEGRAM_TOKEN, WEBHOOK_HOST, WEBHOOK_TOKEN


def commands_callback(update, context):
    time.sleep(1)
    r = requests.get(f"{WEBHOOK_HOST}/commands?token={WEBHOOK_TOKEN}")

    kb_markup = ReplyKeyboardMarkup(
        [[KeyboardButton(com.replace("/", "exec::"))] for com in r.json()]
    )
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Commands fetched successfully !",
        reply_markup=kb_markup,
    )


def exec_callback(update, context):
    expected_command = update.message.text.replace("exec::", "/")
    if "exec::" in update.message.text and len(update.message.text) > 7:
        msg = update.message.reply_text(
            f"Checking your command {update.message.text}..."
        )
        time.sleep(1)
        r = requests.get(f"{WEBHOOK_HOST}/commands?token={WEBHOOK_TOKEN}")
        for com in r.json():
            if com == expected_command:
                req = requests.get(
                    f"{WEBHOOK_HOST}/{expected_command}?token={WEBHOOK_TOKEN}"
                )
                escaped_text = req.text.replace("!", "\\!")
                msg.edit_text(escaped_text, parse_mode="MarkdownV2")
                break
    else:
        update.message.reply_text("Invalid command sent.")


def start_callback(update, context):
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \n" + "Please hit /help to know more about me !",
    )


def help_callback(update, context):
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \n"
        + "Am just a bot that will execute commands for your webhook !\n---\n"
        + "/commands - Get list of your available commands.\n"
        + "/help - help, list of telegram command.\n---\n",
    )


def set_callback():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_callback))
    dispatcher.add_handler(CommandHandler("commands", commands_callback))
    dispatcher.add_handler(CommandHandler("help", help_callback))
    dispatcher.add_handler(MessageHandler(Filters.text, exec_callback))

    return updater

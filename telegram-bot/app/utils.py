import logging
import time

import requests
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from app.settings import AUTHORIZED_USERS, TELEGRAM_TOKEN, WEBHOOK_HOST, WEBHOOK_TOKEN


def is_authorized(update):
    user_name = update.message.from_user["username"]
    if len(user_name) > 1 and user_name in AUTHORIZED_USERS:
        return True
    return False


def is_valid_command(update):
    if "exec::" in update.message.text and 50 > len(update.message.text) > 7:
        return True
    return False


def get_req(url):
    return requests.get(url)


def commands_callback(update, context):
    if is_authorized(update):
        time.sleep(1)
        r = get_req(f"{WEBHOOK_HOST}/commands?token={WEBHOOK_TOKEN}")

        kb_markup = ReplyKeyboardMarkup(
            [[KeyboardButton(com.replace("/", "exec::"))] for com in r.json()]
        )
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Commands fetched successfully !",
            reply_markup=kb_markup,
        )


def exec_callback(update, context):
    try:
        if is_authorized(update) and is_valid_command(update):
            time.sleep(1)
            expected_command = update.message.text.replace("exec::", "/")
            command_url = f"{WEBHOOK_HOST}/{expected_command}?token={WEBHOOK_TOKEN}"
            msg = update.message.reply_text(
                f"Checking your command {update.message.text}..."
            )
            r = get_req(f"{WEBHOOK_HOST}/commands?token={WEBHOOK_TOKEN}")
            for com in r.json():
                if com == expected_command:
                    req = get_req(command_url)
                    escaped_text = req.text.replace("!", "\\!")
                    msg.edit_text(escaped_text, parse_mode="MarkdownV2")
                    break
    except Exception as es:
        logging.exception(f"[x] Error {es}")


def start_callback(update, context):
    if is_authorized(update):
        time.sleep(1)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Hello there, \nPlease hit /help to know more about me !",
        )


def help_callback(update, context):
    if is_authorized(update):
        time.sleep(1)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Hello there, \n"
            + "Am a bot that execute commands from your webhook !\n"
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

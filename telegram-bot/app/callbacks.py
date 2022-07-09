import logging
import time

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.ext.utils.types import CCT
from telegram.message import Message
from telegram.update import Update

from app.settings import TELEGRAM_TOKEN
from app.utils import get_req, is_authorized, is_private, is_valid_command


def clean_msg(context: CCT, update: Update, msg: Message) -> None:
    """
    Clean previous message

    :param context:
    :param update:
    :param msg:
    :return:
    """
    time.sleep(1)
    context.bot.delete_message(
        chat_id=update.message.chat_id, message_id=msg.message_id
    )


def commands_callback(update: Update, context: CCT) -> None:
    """
    The command callback that will return a keyboard of commands

    :param update:
    :param context:
    :return:
    """
    if is_authorized(update) and is_private(update):
        time.sleep(1)
        r = get_req("/commands")

        kb_markup = ReplyKeyboardMarkup(
            [[KeyboardButton(com.replace("/", "exec::"))] for com in r.json()]
        )
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Commands fetched successfully !",
            reply_markup=kb_markup,
        )


def clean_commands_callback(update: Update, context: CCT) -> None:
    """
    Clean the generated keyboard

    :param update:
    :param context:
    :return:
    """
    msg = context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Keyboard Commands cleaned !",
        reply_markup=ReplyKeyboardRemove(),
    )
    # we delete the bot message
    clean_msg(context, update, msg)
    # we delete the user message
    clean_msg(context, update, update.message)


from random import randint


colors = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[37m', '\033[90m', '\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

user_colors = {}

def comment_callback(update: Update, context: CCT) -> None:
    time.sleep(0.3)
    try:
        comment = getattr(update.message, 'text', '---')
        user_name = str(update.message.from_user['username'])

        color_picked = '\033[1;34m'
        if user_name not in user_colors.keys():
            while color_picked in user_colors.values():
                color_picked = colors[randint(0, len(colors))]

            user_colors[user_name] = color_picked

        print(f'{user_colors[user_name]}{user_name}\033[0m : {comment}')
    except Exception:
        pass


def exec_callback(update: Update, context: CCT) -> None:
    """
    Try to execute the incomming command after validating that

    :param update:
    :param context:
    :return:
    """
    try:
        if is_authorized(update) and is_private(update):
            if is_valid_command(update):
                time.sleep(1)
                expected_command = update.message.text.replace("exec::", "/")
                msg = update.message.reply_text(
                    f"Checking your command {update.message.text}..."
                )
                r = get_req("/commands")
                for com in r.json():
                    if com == expected_command:
                        req = get_req(f"/{expected_command}")
                        escaped_msg = req.text.replace("!", "\\!")
                        msg.edit_text(escaped_msg, parse_mode="MarkdownV2")
                        break
    except Exception as es:
        logging.exception(f"[x] Error {es}")


def start_callback(update: Update, context: CCT) -> None:
    """
    The simple start callback to say welcome to the user

    :param update:
    :param context:
    :return:
    """
    if is_authorized(update) and is_private(update):
        time.sleep(1)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Hello there, \nPlease hit /help to know more about me !",
        )


def help_callback(update: Update, context: CCT) -> None:
    """
    The help callback to list available command here

    :param update:
    :param context:
    :return:
    """
    if is_authorized(update) and is_private(update):
        time.sleep(1)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Hello there, \n"
            + "Am a bot that execute commands from your webhook !\n"
            + "/commands - Get list of your available commands.\n"
            + "/help - help, list of telegram command.\n---\n",
        )


def set_callback() -> Updater:
    """
    The setter of all callback that will return an Updater

    :return:
    """
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text, comment_callback))

    return updater

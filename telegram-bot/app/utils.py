import requests
from requests import Response
from telegram.update import Update

from app.settings import AUTHORIZED_USERS, WEBHOOK_HOST, WEBHOOK_TOKEN


def is_private(update: Update) -> bool:
    """
    If it's a private conversation or not

    :param update:
    :return:
    """
    if update.message.chat.type == "private":
        return True
    return False


def is_authorized(update: Update) -> bool:
    """
    If the incomming user is authorized or not

    :param update:
    :return:
    """
    user_name = str(update.message.from_user["username"])
    if len(user_name) > 1 and user_name in AUTHORIZED_USERS:
        return True
    return False


def is_valid_command(update: Update) -> bool:
    """
    If it's a valid command or not

    :param update:
    :return:
    """
    if "exec::" in update.message.text and 50 > len(update.message.text) > 7:
        return True
    return False


def get_req(url: str) -> Response:
    """
    The get requester for our webhook

    :param url:
    :return:
    """
    return requests.get(f"{WEBHOOK_HOST}{url}?token={WEBHOOK_TOKEN}")

from app.utils import set_callback

if __name__ == "__main__":
    updater = set_callback()
    updater.start_polling()
    updater.idle()

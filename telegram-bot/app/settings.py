# First, install configparser using "pip install configparser"
import configparser as Conf

# Configs parameters
configParser = Conf.RawConfigParser()
configParser.read(r"config.txt")

# Filling parameters
WEBHOOK_HOST = configParser.get("conf", "WEBHOOK_HOST")
WEBHOOK_TOKEN = configParser.get("conf", "WEBHOOK_TOKEN")
TELEGRAM_TOKEN = configParser.get("conf", "TELEGRAM_TOKEN")

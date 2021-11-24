# First, install configparser using "pip install configparser"
import configparser as Conf
from typing import List

# Configs parameters
configParser = Conf.RawConfigParser()
configParser.read(r"config.txt")

# Filling parameters
WEBHOOK_HOST: str = configParser.get("conf", "WEBHOOK_HOST")
WEBHOOK_TOKEN: str = configParser.get("conf", "WEBHOOK_TOKEN")
TELEGRAM_TOKEN: str = configParser.get("conf", "TELEGRAM_TOKEN")
AUTHORIZED_USERS: List[str] = ["sanixdarker", "Franck_Mario", "elhmn42"]

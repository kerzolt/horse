import configparser
from enum import Enum

# Config
def get_config():
    cfg = configparser.ConfigParser()
    cfg.read("src/main/resources/config/config.ini")
    return cfg

config = get_config()
DEBUG = config["COMMON"]["DEBUG"].lower() == 'true'

# Enums
class TimeUnit(Enum):
    MINUTE = 0
    HOUR = 1
    DAY = 2
    WEEK = 3
    MONTH = 4
    MAX = 99

class Signal(Enum):
    NONE = 0
    BUY = 1
    SELL = -1


import logging.config
import sys
from fun import readJson

#log設定
logging.config.dictConfig(readJson('log_config'))
logger = logging.getLogger()

def handle_exception(exc_type, exc_value, exc_traceback):
    logger.error("程式碼發生錯誤或例外", exc_info=(exc_type, exc_value, exc_traceback))
sys.excepthook = handle_exception


import random
from fun import writeJson


class genshin_gacha:
    def __init__(self, user):
        self.id = str(user)
        self.data = readJson('gacha')

        if self.id not in self.data:
            self.register()

    def register(self):
        self.data[self.id] = {}
        self.data[self.id]['total_pulls'] = 0


        writeJson('gacha', self.data)

    def pull(self):
        
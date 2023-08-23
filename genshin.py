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
        self.setting = readJson('gacha_setting')

        if self.id not in self.data:
            self.register()

        self.user = self.data[self.id]

        self.tot_pulls = self.user['total_pulls']
        self.pro = self.user['pro']
        self.pity5_pulls = self.user['pity5_pulls']
        self.pity4 = self.user['pity4']
        self.pity4_pulls = self.user['pity4_pulls']
        self.pity4 = self.user['pity4']


    def register(self):
        self.data[self.id] = {}
        self.data[self.id]['total_pulls'] = 0
        self.data[self.id]['pity5_pulls'] = 0
        self.data[self.id]['pity5'] = False
        self.data[self.id]['pity4_pulls'] = 0
        self.data[self.id]['pity4'] = False
        self.data[self.id]['pro'] = self.setting['基礎機率']



        writeJson('gacha', self.data)

    def pull_star(self):
        pro = self.user['pro']
        rand_num = random.random()
        addup_prob = 0

        for star, prob in pro.items():
            addup_prob += prob
            if rand_num < addup_prob:
                return star

    def gacha(self):
        self.user['total_pulls'] += 1
        self.user['pity5_pulls'] += 1
        self.user['pity4_pulls'] += 1 
        writeJson('gacha', self.data)

        if self.user['pity5'] >= self.setting['五星機率增加']:
            self.user['pro']['5'] += 0.06
            writeJson('gacha', self.data)
        
        star = self.pull_star()
        return star
        


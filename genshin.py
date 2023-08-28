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

        self.tot_pulls = self.data[self.id]['total_pulls']
        self.pro = self.user['pro']
        self.pity5_pulls = self.user['pity5_pulls']
        self.pity5 = self.user['pity5']
        self.pity4_pulls = self.user['pity4_pulls']
        self.pity4 = self.user['pity4']
        self.character5 = self.user['character']['5star']
        self.character4 = self.user['character']['4star']

    def update_data(self):
        self.data[self.id]['total_pulls'] = self.tot_pulls
        self.data[self.id]['pro'] = self.pro
        self.data[self.id]['pity5_pulls'] = self.pity5_pulls
        self.data[self.id]['pity5'] = self.pity5
        self.data[self.id]['pity4_pulls'] = self.pity4_pulls
        self.data[self.id]['pity4'] = self.pity4
        self.data[self.id]['character']['5star'] = self.character5
        self.data[self.id]['character']['4star'] = self.character4
        writeJson('gacha', self.data)

    def register(self): # 註冊使用者
        self.data[self.id] = {}
        self.data[self.id]['total_pulls'] = 0
        self.data[self.id]['pity5_pulls'] = 0
        self.data[self.id]['pity5'] = False
        self.data[self.id]['pity4_pulls'] = 0
        self.data[self.id]['pity4'] = False
        self.data[self.id]['pro'] = self.setting['基礎機率']
        self.data[self.id]['character'] = {}
        self.data[self.id]['character']['5star'] = {}
        self.data[self.id]['character']['4star'] = {}

        writeJson('gacha', self.data)

    def pull_star(self): # 抽出星級
        pro = self.user['pro']
        rand_num = random.random()
        addup_prob = 0

        for star, prob in pro.items():
            addup_prob += prob
            if rand_num < addup_prob:
                return star

    def gacha_system(self): #抽卡本體
        self.tot_pulls += 1
        self.pity5_pulls += 1
        self.pity4_pulls += 1

     # 機率改動
        if self.pity5_pulls >= self.setting['五星機率增加']:
            self.user['pro']['5'] += 0.06
            writeJson('gacha', self.data)
        
        star = self.pull_star()        # 取得本次星級

        if star == '5':
            self.pity5_pulls = 0
            self.pro = self.setting['基礎機率']
            if self.pity5 == True:
                up = True
                print(f'pity5: True')               
            else:
                up = random.choice([True, False])
                print(f'pity5: False')
            print(f'up5: {up}')
            if up == True:
                result = self.setting['up五星']
                self.pity5 = False
                
            else:
                result = random.choice(self.setting['常駐五星'])
                self.pity5 = True
            if result not in self.character5:
                self.character5[result] = 1
            else:
                self.character5[result] +=1
                print(f'5result: {result}')

        if star =='4':
            pass # W.I.P.



    def gacha(self):
        self.gacha_system()
        self.update_data() 

    
  
        


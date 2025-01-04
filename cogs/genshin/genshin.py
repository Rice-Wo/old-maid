import random
from collections import defaultdict
import logging


try:
    from .utility import get_data, input_data
except ImportError:
    from utility import get_data, input_data


class genshin_gacha:
    def __init__(self, user: int|str):
        self.id = str(user)
        self.data = get_data('gacha')
        self.setting = get_data('gacha_setting')

        if self.id not in self.data: # 沒有該使用者資料時註冊
            self.register()
        # 登入使用者ID
        self.user = self.data[self.id]
        # 設定變數
        self.tot_pulls: int = self.data[self.id]['total_pulls']
        self.pro: dict = self.user['pro']
        self.pity5_pulls: int = self.user['pity5_pulls']
        self.pity5: bool = self.user['pity5']
        self.pity4_pulls: int = self.user['pity4_pulls']
        self.pity4: bool = self.user['pity4']
        self.genshin5: dict = self.user['genshin']['5star']
        self.genshin4: dict = self.user['genshin']['4star']


    def update_data(self) -> None: #更新資料
        self.data[self.id]['total_pulls'] = self.tot_pulls
        self.data[self.id]['pro'] = self.pro
        self.data[self.id]['pity5_pulls'] = self.pity5_pulls
        self.data[self.id]['pity5'] = self.pity5
        self.data[self.id]['pity4_pulls'] = self.pity4_pulls
        self.data[self.id]['pity4'] = self.pity4
        self.data[self.id]['genshin']['5star'] = self.genshin5
        self.data[self.id]['genshin']['4star'] = self.genshin4
        input_data('gacha', self.data)


    def register(self) -> None: # 註冊使用者
        self.data[self.id] = {}
        self.data[self.id]['total_pulls'] = 0
        self.data[self.id]['pity5_pulls'] = 0
        self.data[self.id]['pity5'] = False
        self.data[self.id]['pity4_pulls'] = 0
        self.data[self.id]['pity4'] = False
        self.data[self.id]['pro'] = self.setting['基礎機率']
        self.data[self.id]['genshin'] = {}
        self.data[self.id]['genshin']['5star'] = {}
        self.data[self.id]['genshin']['4star'] = {}

        input_data('gacha', self.data)


    def pull_star(self) -> str: # 抽出星級
        pro = self.pro
        rand_num = random.random()
        addup_prob = 0

        for star, prob in pro.items():
            addup_prob += prob
            if rand_num < addup_prob:
                return star


    def gacha_system(self) -> dict: #抽卡本體
        self.tot_pulls += 1
        self.pity5_pulls += 1
        self.pity4_pulls += 1

     # 機率改動
        if self.pity5_pulls >= self.setting['五星機率增加']:
            self.pro['5'] += 0.06
            input_data('gacha', self.data)
        elif self.pity4_pulls >= self.setting['四星機率增加']:
            self.pro['4'] = self.setting['四星機率up']
        
        star = self.pull_star() # 取得本次星級
        if self.pity4_pulls >= 10 and star != '5':
            star = '4'

        if star == '5':
            self.pity5_pulls = 0
            self.pro['5'] = self.setting['基礎機率']['5']
            if self.pity5 == True:
                up = True
            else:
                up = random.choice([True, False])
            if up == True:
                result = self.setting['up五星']
                self.pity5 = False
                
            else:
                result = random.choice(self.setting['常駐五星'])
                self.pity5 = True
            if result not in self.genshin5:
                self.genshin5[result] = 1
            else:
                self.genshin5[result] +=1

        if star =='4':
            self.pity4_pulls = 0
            self.pro['4'] = self.setting['基礎機率']['4']
            if self.pity4 == True:
                up = True
            else:
                up = random.choice([True, False])
            if up == True:
                result = random.choice(self.setting['up四星'])
                self.pity4 = False
                
            else:
                result = random.choice(self.setting['常駐四星'])
                self.pity4 = True
            if result not in self.genshin4:
                self.genshin4[result] = 1
            else:
                self.genshin4[result] +=1

        if star == '3':
            result = random.choice(self.setting['三星'])
        output = {}
        output[star] = result
        return output


    def gacha(self) -> dict:
        result = self.gacha_system()
        self.update_data()
        logging.debug(result)
        return result
    
    def ten_gacha(self) -> dict:
        result = defaultdict(list)
        for i in range(10):
            output = self.gacha_system()
            for key, value in output.items():
                result[key].append(value)
        if '4' not in result and '5' not in result:
            random_value = random.choice(result['3'])
            result['3'].remove(random_value)
            # 執行四星抽卡
            self.pity4_pulls = 0
            self.pro['4'] = self.setting['基礎機率']['4']
            if self.pity4 == True:
                up = True
            else:
                up = random.choice([True, False])
            if up == True:
                result = random.choice(self.setting['up四星'])
                self.pity4 = False
                
            else:
                result = random.choice(self.setting['常駐四星'])
                self.pity4 = True
            if result not in self.genshin4:
                self.genshin4[result] = 1
            else:
                self.genshin4[result] +=1
        self.update_data()
        final_result = {key: value for key, value in result.items() if value}

        return final_result
    

if __name__ == '__main__':

    print('現在單獨執行 genshin.py 中')
    user = 'test'
    gacha = genshin_gacha(user)
    
    gacha.ten_gacha()


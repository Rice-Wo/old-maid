import json

def writeJson(file, item): #JSON寫入
    with open(file + '.json', "w+", encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False, indent=4))
   # logging.debug(f'寫入資料至 {file}.json 資料內容{item}')


def readJson(file): #JSON讀取
    with open(file + '.json', "r", encoding='utf-8') as f:
        data = json.load(f)
    return data
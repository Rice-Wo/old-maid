import json
import logging.config

with open('log/log_config.json', "r", encoding='utf-8') as f: # 讀取log設定json檔案
    log = json.load(f)

logging.config.dictConfig(log)
logger = logging.getLogger()

def handle_exception(exc_type, exc_value, exc_traceback): #設定發生問題時的處理方式
    logger.error("程式碼發生錯誤或例外", exc_info=(exc_type, exc_value, exc_traceback))

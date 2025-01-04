from log.logging import handle_exception 
import sys
#報錯設置
sys.excepthook = handle_exception

import discord
from discord.ext import tasks, commands
import random
import jieba
from config import config
from pathlib import Path
import logging
import json

def input_data(file, item): #JSON寫入
    with open('data/'+ file + '.json', "w+", encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False, indent=4))
    logging.debug(f'寫入資料至 {file}.json 資料內容{item}') # 紀錄資料寫入

def get_data(file): #JSON讀取
    with open('data/'+ file + '.json', "r", encoding='utf-8') as f:
        data = json.load(f)
    return data


bot = discord.Bot(status=discord.Status.do_not_disturb, intents = discord.Intents().all())


@bot.event
async def on_ready():
  status.start()
  loaded_cogs = list(bot.cogs.keys())
  if loaded_cogs:
    for cog_name in loaded_cogs:
      logging.info(f'已載入 {cog_name} 模塊')
  else:
    logging.warning('沒有任何模組被載入，請確認cogs資料夾')
  logging.info(f"{bot.user} is online, current version: {config.version}")
  channel = bot.get_channel(config.online_message)
  await channel.send(f"女僕已上線，目前版本 {config.version}")


@tasks.loop(seconds=60)
async def status():
  global chat_data
  chat = get_data('chat')
  await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Game(random.choice(chat["status"])))
  chat_data = chat['chat']


def chat_response(input_string):
    words = ' '.join(jieba.cut(input_string, cut_all=False))
    for response in chat_data:
        if set(words.split()) & set(response['user_input']):
            ans = random.choice(response['bot_response'])
            return ans


@bot.event
async def on_message(msg):
  if msg.author == bot.user:
    return  
  
  elif chat_response(msg.content):
    await msg.channel.send(chat_response(msg.content))



#載入cog
for filepath in Path("./cogs").glob("**/*cog.py"): #載入cog
	parts = list(filepath.parts)
	parts[-1] = filepath.stem
	bot.load_extension(".".join(parts))
	logging.debug(f'已載入 {parts} 模塊')

if __name__ ==  "__main__": #執行機器人
  text = '分詞系統測試成功'
  a = ' '.join(jieba.cut(text, cut_all=False))
  logging.info(a)
  bot.run(config.bot_token)
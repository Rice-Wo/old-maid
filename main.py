from log.logging import handle_exception 
import sys
#抱錯
sys.excepthook = handle_exception

import discord
from discord.ext import tasks, commands
import random
from datetime import timezone,timedelta
import time
import subprocess
import jieba
from fun import *
from pathlib import Path



bot = discord.Bot(status=discord.Status.do_not_disturb, intents = discord.Intents().all())

setting = readJson('setting')
version = setting['version']

@bot.event
async def on_ready():
  status.start()
  loaded_cogs = list(bot.cogs.keys())
  if loaded_cogs:
    for cog_name in loaded_cogs:
      logging.info(f'已載入 {cog_name} 模塊')
  else:
    logging.warning('沒有任何模組被載入，請確認cogs資料夾')
  logging.info(f"{bot.user} is online, current version: {version}")
  token = readJson('token')
  channel = bot.get_channel(token['online'])
  await channel.send(f"女僕已上線，目前版本 {version}")


@tasks.loop(seconds=60)
async def status():
  global chat_data
  chat = readJson('chat')
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

token = readJson('token')


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
  token = readJson('token')
  TOKEN = token['TOKEN']
  bot.run(TOKEN)
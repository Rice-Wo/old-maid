import logging.config
import sys
from fun import readJson

#log設定
logging.config.dictConfig(readJson('log_config'))
logger = logging.getLogger()

def handle_exception(exc_type, exc_value, exc_traceback):
    logger.error("程式碼發生錯誤或例外", exc_info=(exc_type, exc_value, exc_traceback))
sys.excepthook = handle_exception


import discord
from discord.ext import tasks, commands
import random
from datetime import timezone,timedelta
import time
import subprocess
import jieba
from fun import *
from genshin import genshin_gacha
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
guild_ids = token['server']


#載入cog
for filepath in Path("./cogs").glob("**/*.py"):
	cog_name = Path(filepath).stem
	bot.load_extension(f"cogs.{cog_name}")
	logging.debug(f'已載入 {cog_name} 模塊')

if __name__ ==  "__main__": #執行機器人
  text = '分詞系統測試成功'
  a = ' '.join(jieba.cut(text, cut_all=False))
  logging.info(a)
  token = readJson('token')
  TOKEN = token['TOKEN']
  bot.run(TOKEN)
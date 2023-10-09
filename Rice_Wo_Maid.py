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


bot = discord.Bot(status=discord.Status.do_not_disturb, intents = discord.Intents().all())

setting = readJson('setting')
version = setting['version']

@bot.event
async def on_ready():
  status.start()
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





  


















@bot.command(name="user_info使用者資訊", description="展示使用者資訊")  
async def user_info(ctx, member: discord.Member):  # user commands return the member
    name = member.name
    created = member.created_at.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    join = member.joined_at.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    created_time = int(time.mktime(time.strptime(created, "%Y-%m-%d %H:%M:%S")))
    join_time = int(time.mktime(time.strptime(join, "%Y-%m-%d %H:%M:%S")))
    avatar = member.avatar

    embed=discord.Embed(title=f'使用者名稱:{name}', color=member.color)
    if avatar:
      embed.set_thumbnail(url=avatar)
    embed.add_field(name="帳號創建時間", value=f"<t:{created_time}:D>", inline=True)
    embed.add_field(name="加入伺服器時間", value=f"<t:{join_time}:D>", inline=True)
    
    await ctx.respond(embed=embed)


@bot.command(name="avatar頭貼", description='展示指定使用者頭貼')
async def avatar(ctx, member:discord.Member):
  avatar = member.avatar
  if avatar:
    await ctx.respond(f"{member.name}的頭貼:")
    await ctx.send(f"{avatar}")
  else:
    await ctx.respond("這位使用者沒有頭貼")




# 原神抽卡
gacha_setting = readJson('gacha_setting')

@bot.command(name='genshin-10wish原神十抽', description='十抽')
async def gacha10(ctx):
  user_id = ctx.author.id
  gacha = genshin_gacha(user_id)
  result = gacha.ten_gacha()
  if '5' in result:
    color = gacha_setting['5color']
  elif '4' in result: 
    color = gacha_setting['4color']
  else: color = gacha_setting['3color']
  embed=discord.Embed(title='祈願結果',color=color)
  if '5' in result:
   embed.add_field(name='**5星**', value='\n'.join(result['5']), inline=False)
  if '4' in result:
   embed.add_field(name='**4星**', value='\n'.join(result['4']), inline=False)
  embed.add_field(name='**3星**', value='\n'.join(result['3']), inline=False)
  embed.set_footer(text='此為模擬結果僅供參考')
  await ctx.respond(embed=embed)

@bot.command(name='genshin-wish原神單抽', description='單抽')
async def gacha(ctx):
  user_id = ctx.author.id
  gacha = genshin_gacha(user_id)
  result = gacha.gacha()
  if '5' in result:
    color = gacha_setting['5color']
  elif '4' in result: 
    color = gacha_setting['4color']
  else: color = gacha_setting['3color']
  embed=discord.Embed(title='祈願結果',color=color)
  if '5' in result:
   embed.add_field(name='**5星**', value=''.join(result['5']), inline=False)
  if '4' in result:
   embed.add_field(name='**4星**', value=''.join(result['4']), inline=False)
  else: embed.add_field(name='**3星**', value=''.join(result['3']), inline=False)
  embed.set_footer(text='此為模擬結果僅供參考')
  await ctx.respond(embed=embed)

@bot.command(name='genshin-pool原神模擬祈願卡池', description='並不一定是最新的啦.w.')
async def genshin_pool(ctx):
  up_5star = gacha_setting['up五星']
  up_4star = gacha_setting['up四星']
  pool_version = gacha_setting['原神卡池版本']
  five = gacha_setting['常駐五星']
  four = gacha_setting['常駐四星']
  three = gacha_setting['三星']
  embed=discord.Embed(title='原神模擬祈願卡池',description=pool_version,color=discord.Colour.random())
  embed.add_field(name='**up五星**', value=''.join(up_5star), inline=True)
  embed.add_field(name='**up四星**', value=', '.join(up_4star), inline=True)
  embed.add_field(name='**常駐五星**', value=embed_text_adjustment(five), inline=False)
  embed.add_field(name='**常駐四星**', value=embed_text_adjustment(four), inline=True)
  embed.add_field(name='**三星**', value=embed_text_adjustment(three), inline=True)
  embed.set_footer(text='卡池不定時更新')
  await ctx.respond(embed=embed)

@bot.command(name='genshin-showcase原神模擬抽卡角色展示', description='在這裡抽到的都是假的.w.')
async def genshin_showcase(ctx):
  user_id = ctx.author.id
  gacha = genshin_gacha(user_id)
  character5 = gacha.genshin5
  character4 = gacha.genshin4
  name5 = list(character5.keys())
  name4 = list(character4.keys())
  five = []
  four = []  
  for i in name5:
    j = character5[i]
    k = f"{i}：{j}"
    five.append(k)
  for i in name4:
    j = character4[i]
    k = f"{i}：{j}"
    four.append(k)
  
  embed=discord.Embed(title='原神模擬祈願角色展示',description=f'{ctx.author.mention}',color=discord.Colour.random())
  embed.add_field(name='五星', value='\n'.join(five), inline=False)
  embed.add_field(name='四星', value='\n'.join(four), inline=True)
  embed.set_footer(text='在這裡抽到不代表你在遊戲裡能抽到喔~')
  await ctx.respond(embed=embed)
'''
使用者指令們:)
'''

@bot.user_command(name="user_info使用者資訊(使用者指令)")  # create a user command for the supplied guilds
async def user_info(ctx, member: discord.Member):  # user commands return the member
    name = member.name
    created = member.created_at.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    join = member.joined_at.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    created_time = int(time.mktime(time.strptime(created, "%Y-%m-%d %H:%M:%S")))
    join_time = int(time.mktime(time.strptime(join, "%Y-%m-%d %H:%M:%S")))
    avatar = member.avatar

    embed=discord.Embed(title=name, color=member.color)
    if avatar:
     embed.set_thumbnail(url=avatar)
    embed.add_field(name="帳號創建時間", value=f"<t:{created_time}:D>", inline=True)
    embed.add_field(name="加入伺服器時間", value=f"<t:{join_time}:D>", inline=True)
    
    await ctx.respond(embed=embed)


@bot.user_command(name="avatar頭貼(使用者指令)")
async def avatar(ctx, member:discord.Member):
  avatar = member.avatar
  if avatar:
    await ctx.respond(f"{member.name}的頭貼:")
    await ctx.send(f"{avatar}")
  else:
    await ctx.respond("這位使用者沒有頭貼")



if __name__ ==  "__main__": #執行機器人
  text = '分詞系統測試成功'
  a = ' '.join(jieba.cut(text, cut_all=False))
  logging.info(a)
  token = readJson('token')
  TOKEN = token['TOKEN']
  bot.run(TOKEN)
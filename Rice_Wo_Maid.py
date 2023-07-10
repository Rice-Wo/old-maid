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
from fun import writeJson, changeLog, weather_select, chat_update


bot = discord.Bot(status=discord.Status.do_not_disturb, intents = discord.Intents().all())

setting = readJson('setting')

@bot.event
async def on_ready():
  status.start()
  version = setting['version']
  logging.info(f"{bot.user} is online,current {version}")
  Token = readJson('Token')
  channel = bot.get_channel(Token['online'])
  await channel.send(f"女僕已上線，目前版本 {version}")


@tasks.loop(seconds=5)
async def status():
  global chat_data
  await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Game(random.choice(setting["status"])))
  chat_data = readJson('chat')


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

token = readJson('Token')
guild_ids = token['server']

@bot.command(name="test測試", description="測試指令功能用", guild_ids=guild_ids)
@commands.is_owner()
async def test(ctx):
   await ctx.respond('成功')
@test.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
  if isinstance(error, commands.NotOwner):
        await ctx.respond("只有機器人擁有者有權限執行此指令", ephemeral=True)
  else:
      raise error


@bot.command(name="restart重新啟動", description="重啟機器人並下載最新檔案，只適用於Linux", guild_ids=guild_ids)
@commands.is_owner()
async def restart(ctx):
  await ctx.respond("執行成功", ephemeral=True)
  channel = bot.get_channel(setting['online'])
  await channel.send("正在關閉女僕")
  subprocess.run(["python3", "update.py"])
@restart.error
async def on_application_command_eeeor(ctx: discord.ApplicationContext, error: discord.DiscordException):
  if isinstance(error, commands.NotOwner):
        await ctx.respond("只有機器人擁有者有權限執行此指令", ephemeral=True)
  else:
      raise error
  

@bot.command(name='chatdata_update聊天資料更新', description='更新聊天資料', guild_ids=guild_ids)
@commands.is_owner()
async def chatdata_update(ctx,
                          url: discord.Option(str, name='url')):
  chat_update(url)
  await ctx.respond('成功更新聊天資料', ephemeral=True)

@bot.command(name="ping延遲", description='回傳機器人ping值')
async def ping(ctx):
  await ctx.respond(f"目前ping值為 {round(bot.latency * 1000)} ms")


@bot.command(name="random抽籤", description='從指定數字範圍中抽出指定數量的號碼')
async def Random(ctx,
                  最大值: discord.Option(int, min_value=-1000, max_value=1000),
                  最小值: discord.Option(int, min_value=-1000, max_value=1000),
                  times: discord.Option(int, name="抽幾次", min_value=1, max_value=10, default=1)):
    rand = {}
    if 最大值 > 最小值:
      max = 最大值
      min = 最小值
    else:
      max = 最小值
      min = 最大值

    rand[max] = max
    rand[min] = min
    rand[times] = times
    
    if max - min < times:
      await ctx.send("範圍過小，無法抽取")
      return

    def ran(min, max, times):
      number = random.sample(range(min, max), times)
      number.sort()
      result = " , ".join(map(str, number))
      embed=discord.Embed(title='以下為隨機結果', description=result,color=discord.Colour.random())
      embed.set_footer(text=f"抽籤數 {times} 最大值{max} 最小值{min}")
      return embed
    
    class rdbutton(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
      @discord.ui.button(label="再抽一次", style=discord.ButtonStyle.primary) 
      async def button_callback(self, button, interaction):
        await interaction.response.edit_message(embed=ran(rand[min], rand[max], rand[times]), view=rdbutton())

    await ctx.respond(embed=ran(rand[min], rand[max], rand[times]), view=rdbutton())



@bot.command(name="choice選擇", description="幫你從兩個到五個選項中選一個")
async def _choice(ctx,
                  ques: discord.Option(str,"問題是什麼", name="問題"),
                  times: discord.Option(int, name="選項數", min_value=2, max_value=5, default=2)):
  list = []

  def ci(self, interaction: discord.Interaction):
   
    for j in range(len(self.children)):
      value = self.children[j].value
      list.append(value)
    return list

  def rc(ques, list):
    select = " ".join(list)  
    embed=discord.Embed(title=f"關於 {ques} ", color = discord.Colour.random())
    embed.add_field(name=f"{random.choice(list)}", value=f"從 {select} 裡面選一個出來的", inline=False)
    embed.set_footer(text="本結果為隨機選出，僅供參考")
    return embed 
  
  class rcbutton(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="再選一次", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
      await interaction.response.edit_message(embed=rc(ques, list), view=rcbutton())

  class cimodal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for i in range(0, times):
          self.add_item(discord.ui.InputText(label=f"第 {i+1} 個選項"))        

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=rc(ques, ci(self, interaction)), view=rcbutton())

  class cibutton(discord.ui.View):
      @discord.ui.button(label="按這填入選項")
      async def button_callback(self, button, interaction):
          await interaction.response.send_modal(cimodal(title="請輸入選項"))
  
  await ctx.respond(view=cibutton())



@bot.command(name="clean清除訊息",description="一次性刪掉多條訊息")
@discord.default_permissions(manage_messages=True)
async def clean(ctx,
                num: discord.Option(int)):
  await ctx.channel.purge(limit=num)
  await ctx.respond(f"成功刪除 {num} 則訊息", ephemeral=True)



@bot.command(name="updatelog更新日誌", description="取得最新版本的更新內容") #更新日誌
async def _log(ctx):

  button = discord.ui.Button(label="更新日誌", url="https://discord.gg/s6G9nsgeNz")

  view = discord.ui.View()
  view.add_item(button)
    
  embed=discord.Embed(description=changeLog(), color=0x0433ff)
  await ctx.respond(embed=embed, view=view)


@bot.command(name="weather天氣預報", description="取得當前時段的6小時預報")
async def _weather(ctx):
  embed=discord.Embed(title="6小時天氣", description="請從下面選一個地區", color=discord.Colour.random())     
  await ctx.respond(embed=embed, view=weather_select())


@bot.command(name="user_info使用者資訊", description="展示使用者資訊")  # create a user command for the supplied guilds
async def user_info(ctx, member: discord.Member):  # user commands return the member
    name = member
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


@bot.command(name="avatar頭貼")
async def avatar(ctx, member:discord.Member):
  avatar = member.avatar
  if avatar:
    await ctx.respond(f"{member}的頭貼:")
    await ctx.send(f"{avatar}")
  else:
    await ctx.respond("這位使用者沒有頭貼")








'''
使用者指令們:)
'''

@bot.user_command(name="使用者資訊")  # create a user command for the supplied guilds
async def user_info(ctx, member: discord.Member):  # user commands return the member
    name = member
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


@bot.user_command(name="頭貼")
async def avatar(ctx, member:discord.Member):
  avatar = member.avatar
  if avatar:
    await ctx.respond(f"{member}的頭貼:")
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
import discord
from discord.ext import tasks, commands
import random
import requests
from datetime import timezone,timedelta
import time
import subprocess
import jieba
from fun import readJson, writeJson, get_data, changeLog
import logging.config



#log設定
logging.config.dictConfig(readJson('log_config'))
logger = logging.getLogger()


setting = readJson('setting')

if setting['version'].endswith("alpha"):
  bot = discord.Bot(debug_guilds=[911190180260626453],intents = discord.Intents().all())
else:
  bot = discord.Bot(intents = discord.Intents().all())



@bot.event
async def on_ready():
  status.start()
  print(f"{bot.user} is online")
  channel = bot.get_channel(setting['online'])
  version = setting['version']
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
  

@bot.command()
@commands.is_owner()
async def test(ctx):
   await ctx.respond('成功')
@test.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
  if isinstance(error, commands.NotOwner):
        await ctx.respond("Sorry, only the bot owner can use this command!")
  else:
      raise error


@bot.command(name="ping")
async def _ping(ctx):
  await ctx.respond(f"目前ping值為 {round(bot.latency * 1000)} ms")


def check_update():
    # Make a request to the GitHub API to check for updates
    response = requests.get("https://api.github.com/repos/Rice-Wo/Rice-Wo-maid/releases/latest")
    latest_release = response.json()
    latest_version = latest_release["tag_name"]

    # Compare the latest version to the current version
    current_version = setting['version']
    if latest_version > current_version:
        return "有新版本，開始更新"
    else:
        return None

@bot.command(name="restart", description="開發人員專用，只適用於Linux")
@commands.is_owner()
async def update(ctx):
  if ctx.author.id != setting["rice"]:
    await ctx.respond("您不是開發人員")
    return
  else:
    if check_update():
      await ctx.respond("執行成功", ephemeral=True)
      channel = bot.get_channel(setting['online'])
      await channel.send("正在關閉女僕")
      subprocess.run(["python3", "update.py"])
    else:
      await ctx.respond("已經是最新版本", ephemeral=True)

@bot.command(name="random")
async def _random(ctx,
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



@bot.command(name="choice",description="幫你從兩個到五個選項中選一個")
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



@bot.command(name="clean",description="一次性刪掉多條訊息")
@discord.default_permissions(manage_messages=True)
async def _clean(ctx,
                 num: discord.Option(int)):
  await ctx.channel.purge(limit=num)
  await ctx.respond(f"成功刪除 {num} 則訊息", ephemeral=True)



@bot.command(name="更新日誌updatelog") #更新日誌
async def _log(ctx):

  button = discord.ui.Button(label="更新日誌", url="https://discord.gg/s6G9nsgeNz")

  view = discord.ui.View()
  view.add_item(button)
    
  embed=discord.Embed(description=changeLog(), color=0x0433ff)
  await ctx.respond(embed=embed, view=view)



SelectOption = discord.SelectOption



class weather_select(discord.ui.View):
  @discord.ui.select(
    placeholder="地區",
    options=[
    SelectOption(label="宜蘭縣", description='宜蘭縣預報'),
    SelectOption(label="花蓮縣", description='花蓮縣預報'),
    SelectOption(label="臺東縣", description='臺東縣預報'),
    SelectOption(label="澎湖縣", description='澎湖縣預報'),
    SelectOption(label="金門縣", description='金門縣預報'),
    SelectOption(label="連江縣", description='連江縣預報'),
    SelectOption(label="臺北市", description='臺北市預報'),
    SelectOption(label="新北市", description='新北市預報'),
    SelectOption(label="桃園市", description='桃園市預報'),
    SelectOption(label="臺中市", description='臺中市預報'),
    SelectOption(label="臺南市", description='臺南市預報'),
    SelectOption(label="高雄市", description='高雄市預報'),
    SelectOption(label="基隆市", description='基隆市預報'),
    SelectOption(label="新竹縣", description='新竹縣預報'),
    SelectOption(label="新竹市", description='新竹市預報'),
    SelectOption(label="苗栗縣", description='苗栗縣預報'),
    SelectOption(label="彰化縣", description='彰化縣預報'),
    SelectOption(label="南投縣", description='南投縣預報'),
    SelectOption(label="雲林縣", description='雲林縣預報'),
    SelectOption(label="嘉義縣", description='嘉義縣預報'),
    SelectOption(label="嘉義市", description='嘉義市預報'),
    SelectOption(label="屏東縣", description='屏東縣預報')          
  ],
  custom_id='weather'
  )
  async def select_callback(self, select, interaction):
    data = await get_data(select.values[0]) 
    await interaction.response.edit_message(embed=data, view=weather_select())


@bot.command(name="weather")
async def _weather(ctx):
  embed=discord.Embed(title="6小時天氣", description="請從下面選一個地區", color=discord.Colour.random())     
  await ctx.respond(embed=embed, view=weather_select())


@bot.command(name="user_info")  # create a user command for the supplied guilds
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


@bot.command(name="avatar")
async def avatar(ctx, member:discord.Member):
  avatar = member.avatar
  if avatar:
    await ctx.respond(f"{member}的頭貼:")
    await ctx.send(f"{avatar}")
  else:
    await ctx.respond("這位使用者沒有頭貼")


@bot.command(name="r6隨機幹員")
async def R6(ctx):
  def R6pick(side):
    ans = random.choice(setting[side])
    return ans
  class MyView(discord.ui.View):
    @discord.ui.button(label="攻擊方", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        operator = R6pick("R6atk")
        await interaction.response.send_message(operator)

    @discord.ui.button(label="防守方", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        operator = R6pick("R6def")
        await interaction.response.send_message(operator)

  await ctx.respond(view=MyView())








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



if __name__ ==  "__main__":
  text = '分詞系統測試成功'
  a = ' '.join(jieba.cut(text, cut_all=False))
  print(a)
  token = readJson('token')
  TOKEN = token['TOKEN']
  bot.run(TOKEN)
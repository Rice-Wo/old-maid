import discord
from discord import Embed
from discord.ext import commands, tasks
import os
import json
import random
import asyncio
import requests

bot = discord.Bot(debug_guilds=[662586019987587089],status=discord.Status.do_not_disturb, intents = discord.Intents().all())


with open('setting.json', 'r', encoding = "utf-8") as setting:
	setting = json.load(setting)

with open('setting.json', 'r', encoding = "utf-8") as token:
	token = json.load(setting)



@bot.event
async def on_ready():
  status.start()
  print(f"{bot.user} is online")
  

@tasks.loop(seconds=5)
async def status():
  await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Game(random.choice(setting["status"])))



@bot.event
async def on_message(msg):
  if msg.author == bot.user:
    return
  elif msg.content == "test":
    await msg.channel.send("test!")
  



@bot.command(name="test")
async def _test(ctx):
  if ctx.author.id != setting["rice"]:
    await ctx.respond("您不是開發人員")
    return
  else:
    await ctx.respond("i'm still alive :)")

rand = {}
@bot.command(name="random",debug_guilds=[662586019987587089])
async def _random(ctx,
                  最大值: discord.Option(int, min_value=-1000, max_value=1000),
                  最小值: discord.Option(int, min_value=-1000, max_value=1000),
                  times: discord.Option(int, name="抽幾次", min_value=1, max_value=10, default=1)):

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
      @discord.ui.button(label="再抽一次", style=discord.ButtonStyle.primary) # Create a button with the label "😎 Click me!" with color Blurple
      async def button_callback(self, button, interaction):
        await interaction.response.edit_message(embed=ran(rand[min], rand[max], rand[times]), view=rdbutton())

    await ctx.respond(embed=ran(rand[min], rand[max], rand[times]), view=rdbutton())






@bot.command(name="choice",description="幫你從兩個到十個選項中選一個")
async def _choice(ctx,
                  ques: discord.Option(str,"問題是什麼", name="問題"),
                  times: discord.Option(int, name="選項數", min_value=2, max_value=10, default=2)):
  def check(message):
    return message.author == ctx.user and message.channel == ctx.channel and message.author != bot.user
    
  try: 
    
    select= []  

    for a in range(times):
      if a+1 <= len(setting['dinner']):
        dinner = f"例如：{setting['dinner'][a]}"
      else:
        dinner = "沒東西吃了"
        
      embed=discord.Embed(title=f"請輸入第 {a+1} 個選項 ",description=dinner, color=discord.Colour.random())
      embed.set_footer(text="請於20秒內完成輸入")
      await ctx.respond(embed=embed)

      msg2 = await bot.wait_for('message', check=check, timeout=20)
      A = msg2.content
      select.append(A)

      list = " ".join(select)

    def rc(ques, select, list):  
      embed=discord.Embed(title=f"關於 {ques} ", color = discord.Colour.random())
      embed.add_field(name=f"{random.choice(select)}", value=f"從 {list} 裡面選一個出來的", inline=False)
      embed.set_footer(text="本結果為隨機選出，僅供參考")
      return embed
    
    class cibutton(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
      @discord.ui.button(label="再選一次", style=discord.ButtonStyle.primary)
      async def button_callback(self, button, interaction):
        await interaction.response.edit_message(embed=rc(ques,select, list), view=cibutton())

    await ctx.send(embed=rc(ques,select, list), view=cibutton())                
    
  except asyncio.TimeoutError:
    embed=discord.Embed(title="時間已超過", color=0xff2600)
    await ctx.send(embed=embed) 

@bot.command(name="clean",description="一次性刪掉多條訊息")
@discord.default_permissions(manage_messages=True)
async def _clean(ctx,
                 num: discord.Option(int)):
  await ctx.channel.purge(limit=num+1)
  msg = await ctx.respond(f"成功刪除 {num} 則訊息", delete_after=3)

@bot.command(name="updatelog")
async def _log(ctx):
  with open("update.txt", "r", encoding='utf8') as f:
          word = f.read()
  embed=discord.Embed(title="更新日誌", description=word, color=0x0433ff)
  await ctx.respond(embed=embed)


SelectOption = discord.SelectOption







async def get_data(location):

    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": TOKEN,
        "locationName":location
        
    }

    response = requests.get(url, params=params)
    print(response.status_code)

    if response.status_code == 200:
        # print(response.text)
        data = json.loads(response.text)
        
       
        
        locationName = data["records"]["location"][0]["locationName"]
        weather_elements = data["records"]["location"][0]["weatherElement"]
        start_time = weather_elements[0]["time"][0]["startTime"]
        end_time = weather_elements[0]["time"][0]["endTime"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]

        embed=discord.Embed(title=f"{locationName} 的天氣預報", description=f"本預報時段為 {start_time} 到 {end_time}")
        embed.add_field(name="最高溫", value=f"{max_tem} °C" , inline=True)
        embed.add_field(name="最低溫", value=f"{min_tem} °C" , inline=True)
        embed.add_field(name="降雨機率", value=f"{rain_prob} %", inline=False)
        embed.add_field(name=weather_state, value=comfort, inline=True)
        embed.set_footer(text="以上資料由中央氣象局提供")
        
        

    else:
      print("Can't get data!")
      embed=discord.Embed(title=f"錯誤!", description=f"無法取得資料", color = 0xff0000)
      embed.set_footer(text="請稍後再試或是聯繫 稻禾Rice_Wo#3299")
    return embed

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
  embed=discord.Embed(title="6小時天氣", description="請從下面選一個地區", color=0xaaaaaa)     
  await ctx.respond(embed=embed, view=weather_select())















if __name__ ==  "__main__":
  TOKEN = token['TOKEN']
  bot.run(TOKEN)
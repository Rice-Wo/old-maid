import discord
from discord import Embed
from discord.ext import commands, tasks
import os
import json
import random
import asyncio
import requests
import re

bot = discord.Bot(debug_guilds=[911190180260626453],status=discord.Status.do_not_disturb, intents = discord.Intents().all())


with open('setting.json', 'r', encoding = "utf-8") as setting:
	setting = json.load(setting)

with open('Token.json', 'r', encoding = "utf-8") as token:
	token = json.load(token)

with open('chat.json', 'r', encoding = "utf-8") as chat:
	chat_data = json.load(chat)



@bot.event
async def on_ready():
  status.start()
  print(f"{bot.user} is online")
  


@tasks.loop(seconds=5)
async def status():
  await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Game(random.choice(setting["status"])))


def chat_response(input_string):
    message = re.split(r'\s+|[,;?!.-]\s*', input_string)
    unlist = "".join(message)
    split_message = []
    for i in unlist:
        cn = list(i)
        split_message.extend(cn)
    score_list = []

    # Check all the responses
    for response in chat_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in message:
                if word in required_words:
                    required_score += 1
                    print(required_score)

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
            for word in message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        print(response_score, response["user_input"])

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # If there is no good response, return a random one.
    if best_response != 0:
        return chat_data[response_index]["bot_response"]
    
    score_list = []

    # Check all the responses
    for response in chat_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1
                    print(required_score)

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        # print(response_score, response["user_input"])

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # If there is no good response, return a random one.
    if best_response != 0:
        return random.choice(chat_data[response_index]["bot_response"])





@bot.event
async def on_message(msg):
  if msg.author == bot.user:
    return
  elif msg.content == "test":
    await msg.channel.send("test!")
  
  
  elif chat_response(msg.content):
    await msg.channel.send(chat_response(msg.content))
  



@bot.command(name="test")
async def _test(ctx):
  if ctx.author.id != setting["rice"]:
    await ctx.respond("您不是開發人員")
    return
  else:
    await ctx.respond("i'm still alive :)")



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
  await ctx.channel.purge(limit=num+1)
  await ctx.respond(f"成功刪除 {num} 則訊息", delete_after=3)



@bot.command(name="updatelog")
async def _log(ctx):
  with open("update.txt", "r", encoding='utf8') as f:
          word = f.read()

  button = discord.ui.Button(label="更新日誌", url="https://discord.gg/s6G9nsgeNz")

  view = discord.ui.View()
  view.add_item(button)
    
  embed=discord.Embed(title="更新日誌", description=word, color=0x0433ff)
  await ctx.respond(embed=embed, view=view)



SelectOption = discord.SelectOption

async def get_data(location):

    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": token['CWB-TOKEN'],
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
  embed=discord.Embed(title="6小時天氣", description="請從下面選一個地區", color=discord.Colour.random())     
  await ctx.respond(embed=embed, view=weather_select())













if __name__ ==  "__main__":
  TOKEN = token['test']
  bot.run(TOKEN)
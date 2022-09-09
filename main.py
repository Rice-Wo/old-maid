import discord
from discord import Embed
from discord.ext import commands, tasks
import os
import json
import random
import asyncio



from dotenv import load_dotenv
load_dotenv()




bot = discord.Bot(debug_guilds=[662586019987587089],status=discord.Status.do_not_disturb, intents = discord.Intents().all())



with open('setting.json', 'r', encoding = "utf-8") as setting:
	setting = json.load(setting)





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
@bot.slash_command(name="random",debug_guilds=[662586019987587089])
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


@bot.slash_command(name="choice")
async def _choice(ctx,
                  name: discord.Option(str, name="請輸入問題"),
                  times: discord.Option(int, name="選項數量",max_value=10, default=2)):
  def check(message):
    return message.author == ctx.user and message.channel == ctx.channel and message.author != bot.user
    
  try:
    if int(times) <= 1:
      await ctx.send('只有一個選項，那就只能選那個了...')
      return   
    
    select= []  

    for a in range(int(times)):
      if a+1 <= len(setting['dinner']):
        dinner = f"例如：{setting['dinner'][a]}"
      else:
        dinner = "沒東西吃了"
        
      embed=discord.Embed(title=f"請輸入第 {a+1} 個選項 ",description=dinner, color=discord.Colour.random())
      embed.set_footer(text="請於20秒內完成輸入")
      await ctx.send(embed=embed)
      msg2 = await bot.wait_for('message', check=check, timeout=20)
      A = msg2.content
      select.append(A)

      list = " ".join(select)

    def rc(Q, select, list):  
      embed=discord.Embed(title=f"關於 {Q} ", color = discord.Colour.random())
      embed.add_field(name=f"{random.choice(select)}", value=f"從 {list} 裡面選一個出來的", inline=False)
      embed.set_footer(text="本結果為隨機選出，僅供參考")
      return embed
    
    class cibutton(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
      @discord.ui.button(label="再選一次", style=discord.ButtonStyle.primary) # Create a button with the label "😎 Click me!" with color Blurple
      async def button_callback(self, button, interaction):
        await interaction.response.edit_message(embed=rc(Q,select, list), view=cibutton())

    await ctx.send(embed=rc(Q,select, list), view=cibutton())                
    
  except asyncio.TimeoutError:
    embed=discord.Embed(title="時間已超過", color=0xff2600)
    await ctx.send(embed=embed)

















if __name__ ==  "__main__":
  TOKEN = os.environ['TOKEN']
  bot.run(TOKEN)
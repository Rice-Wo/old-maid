import discord
from discord import Embed
from discord.ext import commands, tasks
import os
import json
import random


from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents().all()


bot = discord.Bot(debug_guilds=[662586019987587089],status=discord.Status.do_not_disturb)



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
  



@bot.command()
async def test(ctx):
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















if __name__ ==  "__main__":
  TOKEN = os.environ['TOKEN']
  bot.run(TOKEN)
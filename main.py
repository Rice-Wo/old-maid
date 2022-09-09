import discord
from discord import Embed
from discord.ext import commands, tasks
import os
import json
import random


from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents().all()


bot = discord.Bot(debug_guilds=[843982049877557258],status=discord.Status.do_not_disturb)



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



@bot.command()
async def load(ctx, cog):
  if ctx.author.id != setting["rice"]:
    await ctx.respond("您不是開發人員")
    return
  else:
    bot.load_extension(f"cogs.{cog}")
    await ctx.respond(f"loaded {cog}")
@load.error
async def load_error(ctx, error):
  await ctx.respond(f"load failed")


@bot.command()
async def unload(ctx, cog):
  if ctx.author.id != setting["rice"]:
    await ctx.respond("您不是開發人員")
    return
  else:
    bot.unload_extension(f"cogs.{cog}")
    await ctx.respond(f"unloaded {cog}")
@unload.error
async def unload_error(ctx, error):
  await ctx.respond(f"unload failed")


@bot.command()
async def reload(ctx, cog):
  if ctx.author.id != setting["rice"]:
    await ctx.respond("您不是開發人員")
    return
  else:
    bot.reload_extension(f"cogs.{cog}")
    await ctx.respond(f"reloaded {cog}")
@reload.error
async def reload_error(ctx, error):
  await ctx.respond(f"reload failed")















if __name__ ==  "__main__":
  TOKEN = os.environ['TOKEN']
  bot.run(TOKEN)
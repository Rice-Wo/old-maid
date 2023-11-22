import discord
from discord.ext import commands
import requests
import logging

from utility import get_data, config

"""
所有跟機器人最基本功能有關聯的都在這
"""



class system(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot   
        self.version = config.version

    
    guild_ids = config.admin_server
        
    @discord.slash_command(name="ping")
    async def ping(self, ctx):
        await ctx.respond(f"目前ping值為 {round(self.bot.latency * 1000)} ms")

    @discord.slash_command(name='close')
    @commands.is_owner()
    async def _close(self, ctx):
        await ctx.respond('正在關閉機器人')
        await self.self.bot.close()

    @discord.slash_command(name="test測試", description="測試指令功能用", guild_id=guild_ids)
    @commands.is_owner()
    async def test(self, ctx):
        await ctx.respond(f'成功 目前版本 {self.version}')
        
    @discord.slash_command(name='chatdata_update聊天資料更新', description='更新聊天資料', guild_id=guild_ids)
    @commands.is_owner()
    async def chatdata_update(self, ctx,
                              url: discord.Option(str, name='url')):
        chat_update(url)
        await ctx.respond('成功更新聊天資料', ephemeral=True)
    




    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.NotOwner):
            await ctx.send("只有機器人主人能使用這個指令!")
        else:
            raise error  # Here we raise other errors to ensure they aren't ignored



def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(system(bot)) # add the cog to the self.bot

logging.debug('system had been imported')


def chat_update(url): # 更新聊天資料
    destination = "chat.json"
    try:
        response = requests.get(url)
        with open(destination, 'w', encoding='utf-8') as file:
            file.write(response.text, ensure_ascii=False, indent=4)
        logging.info("成功下載並替換聊天資料")
    except requests.exceptions.RequestException as e:
        logging.error("下載聊天資料時發生錯誤: %s", str(e))
    except Exception as e:
        logging.error("處理聊天資料時發生錯誤: %s", str(e))
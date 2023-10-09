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
from discord.ext import commands
from fun import *

"""
所有跟機器人最基本功能有關聯的都在這
"""



class system(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot   
        self.setting = readJson('setting')
        self.version = self.setting['version']

    token = readJson('token')
    guild_ids = token['server']
        
    @discord.slash_command(name="ping")
    async def ping(self, ctx):
        await ctx.respond(f"目前ping值為 {round(self.bot.latency * 1000)} ms")

    @discord.slash_command(name='close')
    @commands.is_owner()
    async def _close(self, ctx):
        await ctx.respond('正在關閉機器人')
        await self.self.bot.close()

    @discord.slash_command(name="test測試", description="測試指令功能用", guild_ids=guild_ids)
    @commands.is_owner()
    async def test(self, ctx):
        await ctx.respond(f'成功 目前版本 {self.version}')
        
    @discord.slash_command(name='chatdata_update聊天資料更新', description='更新聊天資料', guild_ids=guild_ids)
    @commands.is_owner()
    async def chatdata_update(self, ctx,
                            url: discord.Option(str, name='url')):
        chat_update(url)
        await ctx.respond('成功更新聊天資料', ephemeral=True)
    

    @discord.slash_command(name='load-cog載入模組', description='只有主人能用喵')
    @commands.is_owner()
    async def load(self, ctx, cog):
  
        self.bot.load_extension(f"cogs.{cog}")
        await ctx.respond(f"loaded {cog}")
    @load.error
    async def load_error(self, ctx, error):
        await ctx.respond(f"load failed")


    @discord.slash_command(name='unload-cog卸載模組', description='只有主人能用喵')
    @commands.is_owner()
    async def unload(self, ctx, cog):
        self.bot.unload_extension(f"cogs.{cog}")
        await ctx.respond(f"unloaded {cog}")
    @unload.error
    async def unload_error(self, ctx, error):
      await ctx.respond(f"unload failed")


    @discord.slash_command(name='reload-cog重新載入模組', description='只有主人能用喵')
    @commands.is_owner()
    async def reload(self, ctx, cog):
        
        self.bot.reload_extension(f"cogs.{cog}")
        await ctx.respond(f"reloaded {cog}")
    @reload.error
    async def reload_error(self, ctx, error):
       await ctx.respond(f"reload failed")




    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.NotOwner):
            await ctx.send("只有機器人主人能使用這個指令!")
        else:
            raise error  # Here we raise other errors to ensure they aren't ignored



def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(system(bot)) # add the cog to the self.bot
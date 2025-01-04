import discord
from discord.ext import commands
import random
from datetime import timezone,timedelta
import time
import logging

from .ui import weather_select, changeLog

"""
女僕核心功能
"""



class coc7(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot   

        
    @discord.slash_command(name="random抽籤", description='從指定數字範圍中抽出指定數量的號碼')
    async def Random(self, ctx):
        pass
                    
       


  




def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(coc7(bot)) # add the cog to the bot

logging.debug('maid had been imported')

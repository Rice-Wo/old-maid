import discord
from discord.ext import commands
import requests
import logging

from .utility import get_data
from config import config

"""
21點
"""



class blackjack(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot   
        self.version = config.version

            
    @discord.slash_command(name="play blackjack")
    async def ping(self, ctx):
        await ctx.respond(f"在做了不要催")

    
    




    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.NotOwner):
            await ctx.send("只有機器人主人能使用這個指令!")
        else:
            raise error  # Here we raise other errors to ensure they aren't ignored



def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(blackjack(bot)) # add the cog to the self.bot

logging.debug('blackjack had been imported')



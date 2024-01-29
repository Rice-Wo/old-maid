import discord
from discord.ext import commands
from .utility import get_data, embed_text_adjustment
from .genshin import genshin_gacha
import logging

"""
原神抽卡模擬
"""



class genshin(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot   
        self.gacha_setting = get_data('gacha_setting')


    

    @discord.slash_command(name='genshin-10wish原神十抽', description='十抽')
    async def gacha10(self, ctx):
        user_id = ctx.author.id
        gacha = genshin_gacha(user_id)
        result = gacha.ten_gacha()
        if '5' in result:
            color = self.gacha_setting['5color']
        elif '4' in result: 
            color = self.gacha_setting['4color']
        else: color = self.gacha_setting['3color']
        embed=discord.Embed(title='祈願結果',color=color)
        if '5' in result:
            embed.add_field(name='**5星**', value='\n'.join(result['5']), inline=False)
        if '4' in result:
            embed.add_field(name='**4星**', value='\n'.join(result['4']), inline=False)
            embed.add_field(name='**3星**', value='\n'.join(result['3']), inline=False)
            embed.set_footer(text='此為模擬結果僅供參考')
        await ctx.respond(embed=embed)

    @discord.slash_command(name='genshin-wish原神單抽', description='單抽')
    async def gacha(self, ctx):
        user_id = ctx.author.id
        gacha = genshin_gacha(user_id)
        result = gacha.gacha()
        if '5' in result:
            color = self.gacha_setting['5color']
        elif '4' in result: 
            color = self.gacha_setting['4color']
        else: color = self.gacha_setting['3color']
        embed=discord.Embed(title='祈願結果',color=color)
        if '5' in result:
            embed.add_field(name='**5星**', value=''.join(result['5']), inline=False)
        if '4' in result:
           embed.add_field(name='**4星**', value=''.join(result['4']), inline=False)
        else: embed.add_field(name='**3星**', value=''.join(result['3']), inline=False)
        embed.set_footer(text='此為模擬結果僅供參考')
        await ctx.respond(embed=embed)

    @discord.slash_command(name='genshin-pool原神模擬祈願卡池', description='並不一定是最新的啦.w.')
    async def genshin_pool(self, ctx):
        up_5star = self.gacha_setting['up五星']
        up_4star = self.gacha_setting['up四星']
        pool_version = self.gacha_setting['原神卡池版本']
        five = self.gacha_setting['常駐五星']
        four = self.gacha_setting['常駐四星']
        three = self.gacha_setting['三星']
        embed=discord.Embed(title='原神模擬祈願卡池',description=pool_version,color=discord.Colour.random())
        embed.add_field(name='**up五星**', value=''.join(up_5star), inline=True)
        embed.add_field(name='**up四星**', value=', '.join(up_4star), inline=True)
        embed.add_field(name='**常駐五星**', value=embed_text_adjustment(five), inline=False)
        embed.add_field(name='**常駐四星**', value=embed_text_adjustment(four), inline=True)
        embed.add_field(name='**三星**', value=embed_text_adjustment(three), inline=True)
        embed.set_footer(text='卡池不定時更新')
        await ctx.respond(embed=embed)

    @discord.slash_command(name='genshin-showcase原神模擬抽卡角色展示', description='在這裡抽到的都是假的.w.')
    async def genshin_showcase(self, ctx):
        user_id = ctx.author.id
        gacha = genshin_gacha(user_id)
        character5 = gacha.genshin5
        character4 = gacha.genshin4
        name5 = list(character5.keys())
        name4 = list(character4.keys())
        five = []
        four = []  
        for i in name5:
            j = character5[i]
            k = f"{i}：{j}"
            five.append(k)
        for i in name4:
            j = character4[i]
            k = f"{i}：{j}"
            four.append(k)
        
        embed=discord.Embed(title='原神模擬祈願角色展示',description=f'{ctx.author.mention}',color=discord.Colour.random())
        embed.add_field(name='五星', value='\n'.join(five), inline=False)
        embed.add_field(name='四星', value='\n'.join(four), inline=True)
        embed.set_footer(text='在這裡抽到不代表你在遊戲裡能抽到喔~')
        await ctx.respond(embed=embed)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(genshin(bot)) # add the cog to the bot

logging.debug('genshin_gacha had been imported')

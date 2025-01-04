import discord
from discord.ext import commands
import requests
import logging

from .utility import get_data, list_str, input_data
from config import config
from .blackjack import blackjack_game

"""
21點
"""



class blackjack(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot   
        self.version = config.version
        self.bj = None
        

            
    @discord.slash_command(name="blackjack")
    async def bj(self, ctx):
        self.bj = blackjack_game()
        self.bj.game_start()

        bj_data = get_data('blackjack')
        bj_data['tot'] += 1
        input_data('blackjack', bj_data)

        embed=discord.Embed(title=f'21點', description=f'你的牌：{list_str(self.bj.player_hand)}')
        await ctx.respond(embed=embed, view=MyView(self.bj))

    @discord.slash_command(Name='blackjack-stats')
    async def bj_stats(self, ctx):
        bj_data = get_data('blackjack')
        tot = bj_data['tot']
        com = bj_data['com']
        player = bj_data['player']
        both = bj_data['both']
        giveup = tot-(player+com+both)

        player_win_rate = (player / tot)*100
        com_win_rate = (com / tot)*100
        both_rate = (both / tot)*100
        give_up_rate = (giveup / tot)*100
        desc = f'玩家勝率：{player_win_rate}% \n電腦勝率：{com_win_rate}% \n平手機率：{both_rate}% \n棄賽率：{give_up_rate}%'
        embed=discord.Embed(title=f'21點統計', description=desc)
        embed.set_footer(text=f'總場數：{tot}, 電腦勝場數：{com}, 玩家勝場數：{player}, 平手場數：{both}, 棄賽數：{giveup}')
        await ctx.respond(embed=embed)

    




    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.NotOwner):
            await ctx.send("只有機器人主人能使用這個指令!")
        else:
            raise error  # Here we raise other errors to ensure they aren't ignored



def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(blackjack(bot)) # add the cog to the self.bot

logging.debug('blackjack had been imported')


class MyView(discord.ui.View):
    def __init__(self, bj):
        super().__init__()
        self.bj = bj
        self.bj_data = get_data('blackjack')

    @discord.ui.button(label="抽牌", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        self.bj.game_add_card()
        player = self.bj.player_point
        if player > 21:
            bj_data = get_data('blackjack')
            bj_data['com'] += 1
            input_data('blackjack', bj_data)
            embed=discord.Embed(title=f'勝者 電腦', description=f'玩家點數：{player} \n電腦點數：N/A')
            embed.add_field(name='玩家的牌', value=list_str(self.bj.player_hand), inline=False)
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed=discord.Embed(title=f'21點', description=f'你的牌：{list_str(self.bj.player_hand)}')
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="放棄", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        self.bj.game_end()
        player = self.bj.player_point
        com = self.bj.com_point
        if player == com:
            bj_data = get_data('blackjack')
            bj_data['both'] += 1
            input_data('blackjack', bj_data)
            winner = '平手'
        elif com > 21 or (21-com) > (21-player):
            bj_data = get_data('blackjack')
            bj_data['player'] += 1
            input_data('blackjack', bj_data)
            winner = '玩家'
        else:
            bj_data = get_data('blackjack')
            bj_data['com'] += 1
            input_data('blackjack', bj_data)
            winner = '電腦'
        embed=discord.Embed(title=f'勝者 {winner}', description=f'玩家點數：{player} \n電腦點數：{com}')
        embed.add_field(name='玩家的牌', value=list_str(self.bj.player_hand), inline=False)
        embed.add_field(name='電腦的牌', value=list_str(self.bj.computer_hand), inline=True)
        await interaction.response.edit_message(embed=embed, view=None)
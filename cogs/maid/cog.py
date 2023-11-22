import discord
from discord.ext import commands
from fun import *
import random
from datetime import timezone,timedelta
import time


"""
所有跟機器人最基本功能有關聯的都在這
"""



class maid(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot   

        
    @discord.slash_command(name="random抽籤", description='從指定數字範圍中抽出指定數量的號碼')
    async def Random(self, ctx,
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


    @discord.slash_command(name="choice選擇", description="幫你從兩個到五個選項中選一個")
    async def _choice(self, ctx,
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


    @discord.slash_command(name="clean清除訊息",description="一次性刪掉多條訊息")
    @discord.default_permissions(manage_messages=True)
    async def clean(self, ctx,
                    num: discord.Option(int)):
        await ctx.channel.purge(limit=num)
        await ctx.respond(f"成功刪除 {num} 則訊息", ephemeral=True)


    @discord.slash_command(name="updatelog更新日誌", description="取得最新版本的更新內容") #更新日誌
    async def log(self, ctx):

        button = discord.ui.Button(label="支援伺服器", url="https://discord.gg/s6G9nsgeNz")

        view = discord.ui.View()
        view.add_item(button)
            
        embed=discord.Embed(description=changeLog(), color=0x0433ff)
        await ctx.respond(embed=embed, view=view)


    @discord.slash_command(name="weather天氣預報", description="取得當前時段的6小時預報")
    async def weather(self, ctx):
        embed=discord.Embed(title="6小時天氣", description="請從下面選一個地區", color=discord.Colour.random())     
        await ctx.respond(embed=embed, view=weather_select())

    @discord.slash_command(name="user_info使用者資訊", description="展示使用者資訊")  
    async def user_info(self, ctx, member: discord.Member):  # user commands return the member
        name = member.name
        created = member.created_at.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        join = member.joined_at.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        created_time = int(time.mktime(time.strptime(created, "%Y-%m-%d %H:%M:%S")))
        join_time = int(time.mktime(time.strptime(join, "%Y-%m-%d %H:%M:%S")))
        avatar = member.avatar

        embed=discord.Embed(title=f'使用者名稱:{name}', color=member.color)
        if avatar:
            embed.set_thumbnail(url=avatar)
            embed.add_field(name="帳號創建時間", value=f"<t:{created_time}:D>", inline=True)
            embed.add_field(name="加入伺服器時間", value=f"<t:{join_time}:D>", inline=True)
        
        await ctx.respond(embed=embed)


    @discord.slash_command(name="avatar頭貼", description='展示指定使用者頭貼')
    async def avatar(self, ctx, member:discord.Member):
        avatar = member.avatar
        if avatar:
            await ctx.respond(f"{member.name}的頭貼:")
            await ctx.send(f"{avatar}")
        else:
            await ctx.respond("這位使用者沒有頭貼")
    

    @discord.slash_command(name='commands-list指令列表', description='展示所有指令')
    async def commandlist(self, ctx):
        value="\n".join([str(i+1)+". "+x.name for i,x in enumerate(self.bot.commands)])
        embed=discord.Embed(title='指令列表', description=value)
        embed.set_footer(text='稻禾專用女僕Copyright (c) 2022 - 2023 Rice-Wo')
        await ctx.respond(embed=embed)




def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(maid(bot)) # add the cog to the bot

logging.debug('maid had been imported')

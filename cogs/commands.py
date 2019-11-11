import discord 
import random
from discord.ext import commands

class Commands (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, *args): 
        result = 0
        for item in args:
            result += int(item)
        await ctx.send(result)

    @commands.command()
    async def choose(self, ctx, *, arg): 
        res_array = arg.split(ctx.bot.SPLIT_CHAR)
        await ctx.send(random.choice(res_array))

    @commands.command()
    async def testCommand(self, ctx):
        embed = discord.Embed(title = "title", description = "this is an embed", color = 0xff0000)
        embed.add_field(name = "test1", value = "testing1", inline = False)
        embed.add_field(name = "test5", value = "testing2", inline = True)
        embed.add_field(name = "test4", value = "testing 3", inline = True)
        await ctx.send(embed=embed)

def setup(bot):  
    bot.add_cog(Commands(bot))  
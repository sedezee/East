import discord
import re
import random
import DiscordUtils as dutils
import importlib
from discord.ext import commands

class DevCommands (commands.Cog):
    """For dev use only"""

    def __init__(self, bot): 
        self.bot = bot
    
    def cog_check(self, ctx): 
        return ctx.author.id in ctx.bot.DEV_IDS

    @commands.command(name = 'eval', hidden = True, description = "Evaluate!")
    async def evalCode(self, ctx, *, arg): 
        """Evaluate some code. Probably won't do anything terrible."""
        try: 
            result = str(eval(arg))
            if result is not None and result is not "": 
                result = re.sub(r"([`])", "\\g<1>\u200b", result)
                await ctx.send("```py\n" +  result + "\n```")
        except Exception as e: 
            await ctx.send(f"Program failed with {type(e).__name__}: {e}")
    
    @commands.command(name = 'exec', hidden = True, description = "Execuate!")
    async def execCode(self, ctx, *, arg):
        """Execute some code. Will DEFINITELY do something terrible."""
        try: 
            exec(arg)
        except Exception as e: 
            await ctx.send(f"Program failed with {type(e).__name__}: {e}")

    @commands.command(name = 'stop', hidden = True, description = "D E A T H")
    async def stop(self, ctx): 
        """Or like, breakfast cereal maybe?"""
        randomNum = random.randrange(0,50)
        cereal_array = ["Cookie crisp!", "Frootloops!", "Reese's Puffs!", "Trix!", "Rice Krispee's!", "Apple Jacks!"]
        if randomNum < 49: 
            await ctx.send("Cheerio!")
        else:
            await ctx.send(random.choice(cereal_array))
        await self.bot.logout()
    
    @commands.command(name = 'reload', hidden = True, description = "Reload a cog.")
    async def reload(self, ctx, cog = None):
        short_cog = ['c', 'dc', 'ac']
        if not cog: 
            for cogs in ctx.bot.LOAD_COGS: 
                self.bot.reload_extension(cogs)
            await ctx.send("All cogs reloaded.")
        else:
            if not '_' in cog: 
                cog = dutils.snake_case(cog, False, False)
            if not "cogs." in cog and not cog in short_cog: 
                cog = "cogs." + cog
            if cog in short_cog: 
                for index, item in enumerate(short_cog): 
                    if (cog == item):
                        print(ctx.bot.LOAD_COGS[index])
                        self.bot.reload_extension(ctx.bot.LOAD_COGS[index])
                        await ctx.send(ctx.bot.LOAD_COGS[index] + " reloaded.")
                        
            elif cog in ctx.bot.LOAD_COGS:
                self.bot.reload_extension(cog)
                await ctx.send(cog + " reloaded.")

def setup(bot): 
    bot.add_cog(DevCommands(bot))
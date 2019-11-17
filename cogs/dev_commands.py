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

    @commands.command(name = 'eval', hidden = True)
    async def evalCode (self, ctx, *, arg): 
        try: 
            result = str(eval(arg))
            if result is not None and result is not "": 
                result = re.sub(r"([`])", "\\g<1>\u200b", result)
                await ctx.send("```py\n" +  result + "\n```")
        except Exception as e: 
            await ctx.send(f"Program failed with {type(e).__name__}: {e}")
    
    @commands.command(name = 'stop', hidden = True)
    async def stop(self, ctx): 
        randomNum = random.randrange(0,50)
        cereal_array = ["Cookie crisp!", "Frootloops!", "Reese's Puffs!", "Trix!", "Rice Krispee's!", "Apple Jacks!"]
        if randomNum < 49: 
            await ctx.send("Cheerio!")
        else:
            await ctx.send(random.choice(cereal_array))
        await self.bot.logout()
    
    @commands.command(name = 'reload', hidden = True)
    async def reload(self, ctx, module):
        if not '_' in module: 
            module = dutils.snake_case(module, False, False)
        if "cogs." in module:
            await ctx.send(module + " reloaded.")
            self.bot.reload_extension(module)
        else: 
            await ctx.send("cogs." + module + " reloaded.")
            self.bot.reload_extension("cogs." + module)

    

def setup(bot): 
    bot.add_cog(DevCommands(bot))
import discord
import re
import random
import importlib
from discord.ext import commands
import sedezcompendium.discordtools as dutils


class DevCommands (commands.Cog):
    """For dev use only"""

    def __init__(self, bot): 
        self.bot = bot
    
    def cog_check(self, ctx): 
        return ctx.author.id in ctx.bot.DEV_IDS

    @commands.command(name = 'eval', hidden = True, description = "Evaluate!")
    async def eval_code(self, ctx, *, arg):
        """Evaluate some code. Probably won't do anything terrible."""
        try: 
            result = str(eval(arg))
            if result is not None and result != "":
                result = re.sub(r"([`])", "\\g<1>\u200b", result)
                await ctx.send("```py\n" +  result + "\n```")
        except Exception as e: 
            await ctx.send(f"Program failed with {type(e).__name__}: {e}")
    
    @commands.command(name = 'exec', hidden = True, description = "Execute!")
    async def exec_code(self, ctx, *, arg):
        """Execute some code. Will DEFINITELY do something terrible."""
        try: 
            exec(arg)
        except Exception as e: 
            await ctx.send(f"Program failed with {type(e).__name__}: {e}")

    @commands.command(name = 'stop', hidden = True, description = "D E A T H")
    async def stop(self, ctx): 
        """Or like, breakfast cereal maybe?"""
        random_num = random.randrange(0,50)
        cereal_array = ["Cookie crisp!", "Frootloops!", "Reese's Puffs!", "Trix!", "Rice Krispee's!", "Apple Jacks!"]
        if random_num < 49:
            await ctx.send("Cheerio!")
        else:
            await ctx.send(random.choice(cereal_array))
        await self.bot.logout()
    
    @commands.command(name = 'reload', hidden = True, description = "Reload a cog.")
    async def reload(self, ctx, cog = None):
        short_cog = ['c', 'dc', 'ac', 'jc']
        cog_list = ["cogs.commands", "cogs.dev_commands", "cogs.admin_commands", "cogs.joke_commands"]
        if not cog: 
            for cogs in ctx.bot.LOAD_COGS: 
                self.bot.reload_extension("cogs." + cogs)
            await ctx.send("All cogs reloaded.")
        else:
            if '_' not in cog:
                cog = dutils.snake_case(cog, True)
            if "cogs." not in cog and cog not in short_cog:
                cog = "cogs." + cog
            if cog in short_cog: 
                for index, item in enumerate(short_cog): 
                    if cog == item:
                        self.bot.reload_extension(cog_list[index])
                        await ctx.send(cog_list[index] + " reloaded.")
                        
            elif cog in ctx.bot.LOAD_COGS:
                self.bot.reload_extension(cog)
                await ctx.send(cog + " reloaded.")


def setup(bot): 
    bot.add_cog(DevCommands(bot))

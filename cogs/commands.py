import discord 
import random
from discord.ext import commands

class Commands (commands.Cog):
    """These commands are for general use and can be used by anyone."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = "Adds numbers together.")
    async def add(self, ctx, *args): 
        """Pass in a variable amount of numbers to add, using ``&add 1, 2, 3...``"""
        result = 0.0
        for item in args:
            result += float(item)
        await ctx.send(result)

    @commands.command(description = "Choose between different options")
    async def choose(self, ctx, *, arg): 
        """Choose between any arguments, using ``&choose a, b, c...``. Separate choices with a comma."""
        res_array = arg.split(ctx.bot.SPLIT_CHAR)
        await ctx.send(random.choice(res_array))

    @commands.command(aliases = ["tc"], description = "A test command.")
    async def testCommand(self, ctx):
        """A test command"""
        embed = discord.Embed(title = "title", description = "this is an embed", color = 0xff0000)
        embed.add_field(name = "test1", value = "testing1", inline = False)
        embed.add_field(name = "test5", value = "testing2", inline = True)
        embed.add_field(name = "test4", value = "testing 3", inline = True)
        await ctx.send(embed=embed)

    @commands.command(name = "help", hidden = True)
    async def help(self, ctx, cog): 
        if not cog:  
            embed = discord.Embed(title = "Help", description = "Hello! I'm East. Below are my commands. If you'd like to list a certain category, type ``&help category`` to bring it up.")
            await ctx.send(embed = embed)
        else: 
            cog_list = ["commands", "devcommands", "admincommands"]
            if (cog.lower()) in cog_list: 
                await ctx.send("Here")
                embed = discord.Embed(title = "East Help", description = self.bot.get_cog(cog).description, color = 0xff0000)
                for cItem in self.bot.get_cog(cog).get_commands(): 
                    if not cItem.hidden: 
                        embed.add_field(name = cItem.name, value = cItem.description, inline = False)
                await ctx.send(embed = embed)
def setup(bot):  
    bot.remove_command("help")
    bot.add_cog(Commands(bot))  
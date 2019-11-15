import discord 
import random
import DiscordUtils as dutils
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

    @commands.command(description = "Choose between different options.")
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
    async def help(self, ctx, *, cog = None):
        if not cog:  
            embed = discord.Embed(title = "Help", description = "Hello! I'm East. Below are my commands. If you'd like to list a certain category, type ``&help category`` to bring it up.", color = 0xff0000)
            await ctx.send(embed = embed)
        else: 
            cog = dutils.case(cog, True) 
            cog_list = ["commands", "devcommands", "admincommands"]
            command_list = []
            split_cog = cog.split(" ")
            if split_cog[0].lower() in cog_list: 
                embed = discord.Embed(title = "East Help", description = self.bot.get_cog(split_cog[0]).description, color = 0xff0000)
                for cItem in self.bot.get_cog(split_cog[0]).get_commands(): 
                    if len(split_cog) > 1: 
                        print("HERE")
                        command_list.append(cItem.name)
                    elif not cItem.hidden and len(split_cog) < 2: 
                        embed.add_field(name = cItem.name, value = cItem.description, inline = False)
                for clItem in command_list: 
                    if clItem == split_cog[1]: 
                        #figure out how to pass in the .help value from clItem. it's not 
                        #just clItem because that's only the name, not the actual 
                        #command item. Figure out how to retrieve the command item from 
                        #the above code.
                        embed.add_field(name = clItem, value = , inline = False)
                await ctx.send(embed = embed)
                print(command_list)
            
def setup(bot):  
    bot.remove_command("help")
    bot.add_cog(Commands(bot))  
import discord 
import random
import DiscordUtils as dutils
from discord.ext import commands
import json

with open ("data_storage.json", "r") as file: 
    data = json.load(file)

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
            
    @commands.command(hidden = True, description = "The help command")
    async def help(self, ctx, *, arg = None):
        """The help command."""
        arg = dutils.case(arg, True)
        found = False
        embed = discord.Embed(title = "Help", color = 0xff0000)
        cog_list = ["Commands", "DevCommands", "AdminCommands"]
        for item in cog_list: 
            if not arg:
                found = True
                cog = self.bot.get_cog(item)
                embed.add_field(name = item, value = cog.description, inline = False)
            else: 
                arg_split = arg.split(" ")
                for cItem in self.bot.get_cog(item).get_commands():
                    if len(arg_split) < 2 and arg_split[0].lower() == str(item).lower() and not cItem.hidden:
                        found = True 
                        embed.description = self.bot.get_cog(item).description
                        embed.add_field(name = cItem.name, value = cItem.description, inline = False) 
                    elif (arg_split[-1].lower() == str(cItem).lower() or arg_split[0].lower() == str(cItem).lower()) and not cItem.hidden:
                        if arg_split[0] in cog_list and arg_split[1].lower() == str(cItem).lower():
                            found = True
                            embed.description = cItem.description
                            embed.add_field(name = cItem, value = cItem.help, inline = False)
                        elif arg_split[0].lower() == str(cItem).lower(): 
                            found = True
                            if isinstance(cItem, commands.core.Group):
                                for aItem in ctx.bot.all_commands[arg_split[0]].all_commands.values(): 
                                    print(aItem)
                                    if (str(aItem).lower() == arg.lower()):
                                        embed.description = aItem.description
                                        embed.add_field(name = aItem, value = aItem.help, inline = False)
                                    else: 
                                        embed.description = cItem.description
                                        embed.add_field(name = aItem, value = aItem.description, inline = False)
                            else: 
                                embed.description = cItem.description
                                embed.add_field(name = cItem, value = cItem.help, inline = False)
        if not found: 
            await ctx.send("No such command found. Please use the ``&help [category] [command]`` or ``&help [command]`` format.")
        else: 
            await ctx.send(embed = embed)

    @commands.command(description = "Returns the time for the set timezone.")
    async def time(self, ctx): 
        """Returns the time for the current timezone, which can be set in timezones. Used with ``&time``"""
        time_zone = data[str(ctx.guild.id)]["options"]["time_zone"]
        military_time = data[str(ctx.guild.id)]["options"]["military_time"]
        time_list = dutils.get_time(time_zone, military_time, True)
        if time_list[2] < 10: 
            time_list[2] = "0" + str(time_list[2])
        await ctx.send(f"The time is {time_list[0]}:{time_list[1]}:{time_list[2]}!")


def setup(bot):  
    bot.remove_command("help")
    bot.add_cog(Commands(bot))  
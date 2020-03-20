import discord 
import random
import DiscordUtils as dutils
from discord.ext import commands
import datetime 
import typing 
import json
import time_zone

def east_color(role):
    return role.name.startswith("<East Color")

def talos_color(role):
    return role.name.startswith("<Talos Color>")

def unused_role(ctx, role):
    return (not len(role.members) or (len(role.members) and ctx.author == role.members[0]))

def floating_role(role):
    return not len(role.members)

def command_null_check(self, ctx, command, embed, help = False):
    if command.description != None and command.help != None and help: 
        embed.description = (command.description).replace("&", self.bot.data[str(ctx.guild.id)]["options"]["prefix"])
        embed.add_field(name = command, value = (command.help).replace("&", self.bot.data[str(ctx.guild.id)]["options"]["prefix"]), inline = False)
    elif command.description != None and not help: 
        embed.add_field(name = command, value = (command.description).replace("&", self.bot.data[str(ctx.guild.id)]["options"]["prefix"]), inline = False)
    else: 
        embed.add_field(name = command, value = "", inline = False)
#TODO: Replace extraneous portions with command_null_check 

class Commands(commands.Cog):
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

    @commands.group(alias = ["colour"], description = "Adds a color role to the user.", invoke_without_command = True)
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles = True)
    async def color(self, ctx, *, color: typing.Union[commands.ColourConverter, None]): 
        """Add a color role to yourself using rgb or hex values. Format: ``&color [hex code]``"""
        while(True):
            if color is None: 
                await ctx.send("Sorry, that's not a valid color role.")
                break
                
            #removes prior color roles that have been assigned
            for role in ctx.author.roles: 
                if talos_color(role) or east_color(role):
                    await ctx.author.remove_roles(role)
                    if unused_role(ctx, role):
                        await role.delete() 
            
            break

        color_role = await ctx.guild.create_role(name = f"<East Color {color}>", colour = color)
        await ctx.author.add_roles(color_role)
        await ctx.send("Color added!")
    
    @color.command(name = "remove", description = "Remove your color roles.")
    async def _remove(self, ctx):
        """Removes all of the color roles you may have that are from either East or Talos."""
        for role in ctx.author.roles: 
            if east_color(role) or talos_color(role): 
                await ctx.author.remove_roles(role)
                if unused_role(ctx, role): 
                    await role.delete()
        
        await ctx.send("Color roles removed.")

    @color.command(name = "clear", description = "Removes all unused color roles from the server.")
    async def _clear(self, ctx):
        """Clears all roles from the server. A backup command in case East fails to clear the role correctly upon removal."""
        for role in ctx.guild.roles: 
            if floating_role(role): 
                await role.delete()
        
        await ctx.send("All unused color roles cleared.")

    @commands.command(aliases = ["tc"], description = "A test command.", hidden = True)
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
        #Please note that the below is not the suggested way to execute 
        #a help command. I wrote the help command the way I did for the learning
        #experience and nothing more. If you are looking at East for a reference, 
        #know that this part of the code is not recommended for that purpose. 
        arg = dutils.case(arg, True)
        found = False
        embed = discord.Embed(title = "Help", color = 0xff0000)
        cog_list = ["Commands", "DevCommands", "AdminCommands", "JokeCommands"]

        for item in cog_list: 
            if not arg:
                found = True
                cog = self.bot.get_cog(item)
                embed.add_field(name = item, value = cog.description, inline = False)
            else: 
                arg_split = arg.split(" ")
                for cItem in self.bot.get_cog(item).get_commands():
                    #search through every command
                    if arg_split[-1].lower() == str(item).lower() and not cItem.hidden:
                        #if the last element of the user input equals a cog and it is not hidden, add every command in said cog
                        found = True 
                        embed.description = self.bot.get_cog(item).description
                        embed.add_field(name = cItem.name, value = cItem.description, inline = False) 
                    elif (arg_split[-1].lower() == str(cItem).lower() or arg_split[0].lower() == str(cItem).lower()) and not cItem.hidden:
                        #otherwise, if the last element of user input is equal to an item in the cog OR the first item is equivilent to an item in the cog 
                        found = True
                        if isinstance(cItem, commands.core.Group):
                            #if that command is a group
                            found_commands = []
                            run = True
                            for aItem in ctx.bot.all_commands[arg_split[0].lower()].all_commands.values(): 
                                if len(arg_split) == 1 and not aItem in found_commands:
                                    found_commands.append(aItem)
                                    embed.description = cItem.description
                                    command_null_check(self, ctx, aItem, embed)
                                elif len(arg_split) > 1 and aItem.name.lower() == arg_split[1].lower() and run and aItem.parent.name.lower() == arg_split[0].lower():
                                    run = False
                                    command_null_check(self, ctx, aItem, embed, True)
                                        
                        else: 
                            embed.description = cItem.description
                            embed.add_field(name = cItem, value = (cItem.help).replace("&", self.bot.data[str(ctx.guild.id)]["options"]["prefix"]), inline = False)
        if not found: 
            await ctx.send("No such command found. Please use the ``&help [category] [command]`` or ``&help [command]`` format.")
        else: 
            await ctx.send(embed = embed)

    @commands.group(description = "Registers a virtual scoreboard for the server. Points may be given at will.", invoke_without_command = True)
    @commands.guild_only()
    async def scoreboard(self, ctx):
        """Shows the scoreboard for the server."""
        return 
    
    @commands.command(description = "Returns the time for the set timezone.")
    async def time(self, ctx, time_zone_var = None): 
        """Returns the time for the current timezone, which can be set in timezones. Used with ``&time``"""
        if not time_zone_var: 
            time_zone_var = self.bot.data[str(ctx.guild.id)]["options"]["time_zone"]
        else: 
            time_zone_var = time_zone_var.upper()
            time_zone_var = dutils.to_time_zone(time_zone_var)
            if not isinstance(time_zone_var, time_zone.TimeZone): 
                await ctx.send("Sorry, that's not a valid time zone. I'll be proceeding with your default time zone.")
                time_zone_var = self.bot.data[str(ctx.guild.id)]["options"]["time_zone"]

        military_time = self.bot.data[str(ctx.guild.id)]["options"]["military_time"]
        time_list = dutils.get_time(time_zone_var, military_time, True)
        
        if time_list[2] < 10: 
            time_list[2] = "0" + str(time_list[2])
        
        await ctx.send(f"The time is {time_list[0]}:{time_list[1]}:{time_list[2]}!")

    @commands.command(description = "Gives the time to a certain date.")
    async def timeUntil(self, ctx, unit = "days", month = 0, day = 0, year = 0):
        """Returns the time until a specific date in format ``unit month day year``. Unit may be represented as days, or weeks. Months and years are not currently supported."""
        current_date = datetime.datetime.now()
        to_date = datetime.datetime(year = year, month = month, day = (day + 1))
        time_delta = to_date - current_date
        
        day_string = "days"
        week_string = "weeks"
        weeks = int(time_delta.days / 7)
        days = time_delta.days % 7

        if not month or not day or not year: 
            await ctx.send("Please enter a valid date format: ``dd mm yyyy``.")
        elif time_delta.days == 0: 
            await ctx.send("That's today!")
        elif unit == "days":
            if abs(time_delta.days) == 1: 
                day_string = "day"
        
            if time_delta.days < 0:
                await ctx.send(f"{abs(time_delta.days)} {day_string} since {month}-{day}-{year}.")
            else:
                await ctx.send(f"{time_delta.days} {day_string} until {month}-{day}-{year}.") 
        elif unit == "weeks":
            
            if abs(days) == 1: 
                day_string = "day"

            if abs(weeks) == 1: 
                week_string = "week"
            
           
            if time_delta.days < 0: 
                await ctx.send(f"It has been {weeks} {week_string} and {days} {day_string} since {month}-{day}-{year}.  ")
            else: 
                await ctx.send(f"You have {weeks} {week_string} and {days} {day_string} until {month}-{day}-{year}.")
                
    @commands.command(description = "how fucked you are!", hidden = True)
    async def howFucked(self, ctx, wage = 0, hours_working = 0, days_to_earn = 0, amount_wanted = 0):
        """Returns how fucked you are."""
        weekly_wage = wage * hours_working
        weeks_to_earn = days_to_earn / 7
        amount_earned = weekly_wage * weeks_to_earn
        if(amount_earned < amount_wanted):
            await ctx.send(f"You're fucked! \nWW: {weekly_wage}\nWTE: {weeks_to_earn}\nAE: {amount_earned}")
        else:
            await ctx.send(f"Surprisingly, you might be okay? \nWW: {weekly_wage}\nWTE: {weeks_to_earn}\nAE: {amount_earned}")


def setup(bot):  
    bot.remove_command("help")
    bot.add_cog(Commands(bot))  
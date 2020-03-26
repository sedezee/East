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


def command_null_check(self, ctx, command, embed, help=False):
    if command.description != None and command.help != None and help:
        embed.description = (command.description).replace("&", ctx.prefix)
        embed.add_field(name=command, value=(command.help).replace("&", ctx.prefix), inline=False)
    elif command.description != None and not help:
        embed.add_field(name=command, value=(command.description).replace("&", ctx.prefix), inline=False)
    else:
        embed.add_field(name=command, value="", inline=False)


# TODO: Replace extraneous portions with command_null_check

class Commands(commands.Cog):
    """These commands are for general use and can be used by anyone."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Adds numbers together.")
    async def add(self, ctx, *args):
        """Pass in a variable amount of numbers to add, using ``&add 1, 2, 3...``"""
        result = 0.0
        for item in args:
            result += float(item)
        await ctx.send(result)

    @commands.command(description="Choose between different options.")
    async def choose(self, ctx, *, arg):
        """Choose between any arguments, using ``&choose a, b, c...``. Separate choices with a comma."""
        res_array = arg.split(ctx.bot.SPLIT_CHAR)
        await ctx.send(random.choice(res_array))

    @commands.group(alias=["colour"], description="Adds a color role to the user.", invoke_without_command=True)
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    async def color(self, ctx, *, color: typing.Union[commands.ColourConverter, None]):
        """Add a color role to yourself using rgb or hex values. Format: ``&color [hex code]``"""
        while (True):
            if color is None:
                await ctx.send("Sorry, that's not a valid color role.")
                break

            # removes prior color roles that have been assigned
            for role in ctx.author.roles:
                if talos_color(role) or east_color(role):
                    await ctx.author.remove_roles(role)
                    if unused_role(ctx, role):
                        await role.delete()

            break

        color_role = await ctx.guild.create_role(name=f"<East Color {color}>", colour=color)
        await ctx.author.add_roles(color_role)
        await ctx.send("Color added!")

    @color.command(name="remove", description="Remove your color roles.")
    async def _remove(self, ctx):
        """Removes all of the color roles you may have that are from either East or Talos."""
        for role in ctx.author.roles:
            if east_color(role) or talos_color(role):
                await ctx.author.remove_roles(role)
                if unused_role(ctx, role):
                    await role.delete()

        await ctx.send("Color roles removed.")

    @color.command(name="clear", description="Removes all unused color roles from the server.")
    async def _clear(self, ctx):
        """Clears all roles from the server. A backup command in case East fails to clear the role correctly upon removal."""
        for role in ctx.guild.roles:
            if floating_role(role):
                await role.delete()

        await ctx.send("All unused color roles cleared.")

    @commands.command(description="Returns the time for the set timezone.")
    async def time(self, ctx, selected_zone=None):
        """Returns the time for the current timezone, which can be set in timezones. Used with ``&time``"""
        if selected_zone is None or not isinstance(dutils.to_time_zone(selected_zone.upper()), time_zone.TimeZone):
            if selected_zone is not None: 
                await ctx.send("Sorry, that time zone could not be found, so I'll be proceeding with the default for your server!")
            self.bot.db.execute("""
            SELECT time_zone FROM options
            WHERE guild_id = %s""",
                (str(ctx.guild.id),))
            selected_zone = self.bot.db.fetchone()[0]

        self.bot.db.execute("""
        SELECT military_time FROM options
        WHERE guild_id = %s""",
            (str(ctx.guild.id),))
        military_time = self.bot.db.fetchone()[0]

        time_list = dutils.get_time(selected_zone, military_time, True)

        if time_list[2] < 10:
            time_list[2] = "0" + str(time_list[2])

        await ctx.send(f"The time is {time_list[0]}:{time_list[1]}:{time_list[2]}!")

    @commands.command(description="Gives the time to a certain date.")
    async def timeUntil(self, ctx, unit="days", month=0, day=0, year=0):
        """Returns the time until a specific date. Format to trigger is ``&unit month day year``. Unit may be represented as days, or weeks. Months and years are not currently supported."""
        current_date = datetime.datetime.now()
        to_date = datetime.datetime(year=year, month=month, day=(day + 1))
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
                await ctx.send(
                    f"It has been {weeks} {week_string} and {days} {day_string} since {month}-{day}-{year}.  ")
            else:
                await ctx.send(f"You have {weeks} {week_string} and {days} {day_string} until {month}-{day}-{year}.")

    @commands.command(description="how fucked you are!", hidden=True)
    async def howFucked(self, ctx, wage=0, hours_working=0, days_to_earn=0, amount_wanted=0):
        """Returns how fucked you are."""
        weekly_wage = wage * hours_working
        weeks_to_earn = days_to_earn / 7
        amount_earned = weekly_wage * weeks_to_earn
        if (amount_earned < amount_wanted):
            await ctx.send(f"You're fucked! \nWW: {weekly_wage}\nWTE: {weeks_to_earn}\nAE: {amount_earned}")
        else:
            await ctx.send(
                f"Surprisingly, you might be okay? \nWW: {weekly_wage}\nWTE: {weeks_to_earn}\nAE: {amount_earned}")


def setup(bot):
    # bot.remove_command("help")
    bot.add_cog(Commands(bot))  
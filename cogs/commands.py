import discord
import random
from discord.ext import commands
import datetime
import typing
import utils as dutils
from EastSql import ScoreboardRow, ScoreboardTable, OptionsRow, ScoreStore, StoreItem, ScoreStoreTable
import sedezcompendium.discordtools as dutils

# TODO: improve imports
def east_color(role):
    return role.name.startswith("<East Color")


def talos_color(role):
    return role.name.startswith("<Talos Color>")


def unused_role(ctx, role):
    return not len(role.members) or (len(role.members) and ctx.author == role.members[0])


def floating_role(role):
    return not len(role.members)


def command_null_check(self, ctx, command, embed, help_wanted=False):
    if command.description is not None and command.help is not None and help_wanted:
        embed.description = command.description.replace("&", ctx.prefix)
        embed.add_field(name=command, value=command.help.replace("&", ctx.prefix), inline=False)
    elif command.description is not None and not help_wanted:
        embed.add_field(name=command, value=command.description.replace("&", ctx.prefix), inline=False)
    else:
        embed.add_field(name=command, value="", inline=False)


# TODO: Replace extraneous portions with command_null_check

class Commands(commands.Cog):
    """These commands are for general use and can be used by anyone."""

    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.database

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

    @commands.group(aliases=["colour"], description="Adds a color role to the user.", invoke_without_command=True)
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
    async def clr_remove(self, ctx):
        """Removes all of the color roles you may have that are from either East or Talos."""
        for role in ctx.author.roles:
            if east_color(role) or talos_color(role):
                await ctx.author.remove_roles(role)
                if unused_role(ctx, role):
                    await role.delete()

        await ctx.send("Color roles removed.")

    @color.command(name="clear", description="Removes all unused color roles from the server.")
    async def clr_clear(self, ctx):
        """
        Clears all roles from the server.
        A backup command in case East fails to clear the role correctly upon removal.
        """
        for role in ctx.guild.roles:
            if floating_role(role):
                await role.delete()

        await ctx.send("All unused color roles cleared.")

    @commands.group(description = "The main grouping for East's scoring functionality.")
    @commands.guild_only()
    async def score(self, ctx):
        """A scoreboard with the option to show both positive and negative points."""

    @score.command(name="givePoints", description="Awards a user any number of points.")
    async def score_give_points(self, ctx, user: typing.Union[discord.User, None], point_num: typing.Union[float], complex_remove = False):
        """Gives a specified user any number of specified points. Format is ``&scoreboard givePoints @user number_points``."""
        options_db = self.database.get_item(OptionsRow, guild_id=f"'{ctx.guild.id}'")
        scoreboard_limit = getattr(options_db, "scoreboard_pl")
        scoreboard_db = self.database.get_items(ScoreboardTable, guild_id=f"'{ctx.guild.id}'")
        print(len(scoreboard_db))
        scoreboard_complex = getattr(options_db, "complex_scoring")
        if user is not None and point_num is not None and abs(point_num) < scoreboard_limit:
            points = "point" if abs(point_num) == 1 else "points"

            if abs(point_num) != point_num:
                scoreboard_row = ScoreboardRow(f"'{ctx.guild.id}'", f"'{user.id}'", point_num, 0, 0)
            else:
                scoreboard_row = ScoreboardRow(f"'{ctx.guild.id}'", f"'{user.id}'", 0, point_num, 0)

            self.database.manage_user_points(scoreboard_db, scoreboard_row, not (complex_remove and scoreboard_complex))

            await ctx.send(f"Points updated!")
        else:
            await ctx.send("Sorry, something went wrong. Check the point limit and your formatting!");

    @score.command(name="give", description="Gives a specified user one point.")
    async def score_give(self, ctx, user: typing.Union[discord.User, None], point_num: typing.Union[float] = 1.0):
        """Gives a user a single point. Formatting is: ``&givePoint @User``."""
        await self.score_give_points(ctx, user, point_num)

    @score.command(name="take", description="Gives a specified user one point.")
    async def score_take(self, ctx, user: typing.Union[discord.User, None], point_num: typing.Union[float] = 1.0):
        """Gives a user a single point. Formatting is: ``&givePoint @User``."""
        await self.score_give_points(ctx, user, -abs(point_num))

    @score.command(name="clear", description = "Clears the scoreboard.")
    async def score_clear(self, ctx):
        """Deletes all of the saved scoreboard data for the server."""
        self.database.remove_rows(ScoreboardRow, guild_id=f"'{ctx.guild.id}'")
        await ctx.send("Scoreboard cleared.")

    @score.command(name="show", aliases=["list"], description = "Shows the scoreboard.")
    async def score_show(self, ctx, user = None):
        """Shows the scoreboard. Currently not in any kind of ordered format."""
        # TODO: get this ordered
        scoreboard_data = self.database.get_items(ScoreboardTable, guild_id=f"'{ctx.guild.id}'")
        options_row = self.database.get_item(OptionsRow, guild_id = f"'{ctx.guild.id}'")
        show_neg = getattr(options_row, "show_neg_points")

        embed = discord.Embed(title="Scoreboard", color=0xff0000)
        entries = 9
        i = 0
        if user is None:
            for score_user in scoreboard_data:
                i += 1
                field_str = f'Points: {getattr(score_user, "pos_points") + getattr(score_user, "neg_points")}' if not show_neg else f'Pos points: {getattr(score_user, "pos_points")} \n Neg points: {getattr(score_user, "neg_points")}'
                field_user = self.bot.get_user(int(getattr(score_user, "user_id"))).display_name
                embed.add_field(name = field_user, value = field_str, inline = False)
                if i > entries:
                    break

        await ctx.send(embed = embed)

    @score.command(name = "removeNeg", aliases = ["rmNeg"], hidden = True, description = "Removes negative points.")
    async def score_rmNeg(self, ctx, user: typing.Union[discord.User, None], point_num: typing.Union[float] = -1.0):
        """Remove negative points. Complex scoring only."""
        options_db = self.database.get_item(OptionsRow, guild_id=f"'{ctx.guild.id}'")
        complex_scoring = getattr(options_db, "complex_scoring")
        if not complex_scoring:
            await ctx.send("Sorry, your server doesn't have complex scoring turned on.")
        else:
            await self.score_give_points(ctx, user, -abs(point_num), True)

    @score.command(name = "removePos", aliases = ["rmPos"], hidden = True, description = "Remove positive points.")
    async def score_rmPos(self, ctx, user: typing.Union[discord.User, None], point_num: typing.Union[float] = -1.0):
        """Remove positive points. Complex scoring only."""
        options_db = self.database.get_item(OptionsRow, guild_id=f"'{ctx.guild.id}'")
        complex_scoring = getattr(options_db, "complex_scoring")
        if not complex_scoring:
            await ctx.send("Sorry, your server doesn't have complex scoring turned on.")
        else:
            await self.score_give_points(ctx, user, abs(point_num), True)

    @score.command(name = "storeAdd", description = "Add an item to the store.")
    async def score_store_add(self, ctx, title, desc, price = 0):
        """
        Add an item to the store. Complex scoring only. Looks for a title, a description, and a point price.
        Point price can be either negative or positive.
        """
        store_item = StoreItem(ctx.guild.id, title, desc, price, price == abs(price))
        self.database.insert_item(store_item.to_row())
        await ctx.send("Item added!")

    @score.command(name = "storeRemove", description = "Remove an item from the store.")
    async def score_store_remove(self, ctx, title, price):
        """
        Removes an item from the store. Complex scoring only.
        Uses title and price to differentiate between objects with the same name.
        """
        self.database.remove_rows(ScoreStore, guild_id = f"'{ctx.guild.id}'", title = f"'{title}'", price = price)
        await ctx.send("Item removed!")

    @score.command(name = "storeClear", description = "Remove all items from the store.")
    async def score_store_clear(self, ctx):
        """Clears all items from the store."""
        self.database.remove_rows(ScoreStore, guild_id = f"'{ctx.guild.id}'")
        await ctx.send("Store cleared!")

    @score.command(name = "storeShow", description = "See the store")
    async def score_store_show(self, ctx, title = None):
        """Show the items in the store. Complex scoring only."""
        # TODO fix the pagination on East at some point
        score_rows = self.database.get_items(ScoreStoreTable, guild_id = f"'{ctx.guild.id}'")
        embed = discord.Embed(title = "store", color = 0xff0000)

        for row in score_rows:
            score_store = StoreItem.from_row(row)
            if title is None:
                embed.add_field(name = score_store.title, value = score_store.price, inline = False)
            elif title == score_store.title:
                embed.title = score_store.title
                embed.add_field(name = "Price", value = score_store.price, inline = False)
                embed.add_field(name = "Description", value = score_store.desc, inline = False)
                await ctx.send(embed = embed)
                return

        await ctx.send(embed = embed)

    @score.command(name = "storeBuy", aliases = ["buy"], description = "Buy an item in the store")
    async def score_store_buy(self, ctx, title, price = None):
        """Buy an item from the store! If you need to specify between two items with the same name, plug in the price."""
        score_row = self.database.get_item(ScoreStore,  guild_id = f"'{ctx.guild.id}'", title = f"'{title}'") if price is None else self.database.get_item(ScoreStore,  guild_id = f"'{ctx.guild.id}'", title = "title", price = price)
        store_item = StoreItem.from_row(score_row)
        user = self.bot.get_user(ctx.message.author.id)
        if abs(store_item.price) != store_item.price:
            await self.score_rmNeg(ctx, user, store_item.price)
        else:
            await self.score_rmPos(ctx, user,  store_item.price)

    @score.command(name = "storeRoulette",  aliases= ["roulette"], description = "Run through all of the options.")
    async def score_store_roulette(self, ctx, pos: typing.Union[bool] = False):
        """A roulette of items to buy. Beware, this command will take points you don't have."""
        store_items = self.database.get_items(ScoreStore, guild_id = f"'{ctx.guild.id}'", pos = pos)
        store_item = StoreItem.from_row(random.sample(list(store_items), 1)[0])
        await ctx.send(f"Roulette chose: {store_item.title} for {store_item.price}.")
        user = self.bot.get_user(ctx.message.author.id)
        if abs(store_item.price) != store_item.price:
            await self.score_rmNeg(ctx, user, store_item.price)
        else:
            await self.score_rmPos(ctx, user,  store_item.price)

    @commands.command(description="Returns the time for the set timezone.")
    async def time(self, ctx, selected_zone=None):
        """Returns the time for the current timezone, which can be set in timezones. Used with ``&time``"""
        timezone_db = self.database.get_item(OptionsRow, guild_id=f"'{ctx.guild.id}'")

        try:
            selected_zone = dutils.timezone.TimeZone(selected_zone)
        except (ValueError, TypeError) as e:
            if isinstance(e, ValueError):
                await ctx.send(
                    "Sorry, that time zone could not be found, so I'll be proceeding with the default for your server!")
            selected_zone = getattr(timezone_db, "time_zone")
            selected_zone = dutils.timezone.TimeZone(selected_zone)

        military_time = getattr(timezone_db, "military_time")

        time_list = dutils.get_time(selected_zone, military_time, True)

        if time_list[2] < 10:
            time_list[2] = "0" + str(time_list[2])

        await ctx.send(f"The time is {time_list[0]}:{time_list[1]}:{time_list[2]}!")

    @commands.command(description = "Get time to a date.")
    async def timeTo(self, ctx, *args):
        """Get the time to an event. Uses the date format specified in East's options."""
        args = list(args)
        unit = None

        try:
            int(args[0])
        except (ValueError, IndexError):
            if len(args) > 1 and (args[0] == "weeks" or args[0] == "days"):
                unit = args[0]
                old_args = args
                for index in range(len(old_args) - 1):
                    args[index] = old_args[index + 1]

                args.pop()

        options_row = self.database.get_item(OptionsRow, guild_id = f"'{ctx.guild.id}'")
        date_format = getattr(options_row, "date_format")
        months = {
            "JANUARY": 1,
            "FEBRUARY": 2,
            "MARCH": 3,
            "APRIL": 4,
            "MAY": 5,
            "JUNE": 6,
            "JULY": 7,
            "AUGUST": 8,
            "SEPTEMBER": 9,
            "OCTOBER": 10,
            "NOVEMBER": 11,
            "DECEMBER": 12
        }

        if len(args) == 0:
            to_date = dutils.utils.date_format("MM-DD-YY", "08-20-2020")
            args_str = "08-20-2020"
        elif len(args) == 1:
            to_date = dutils.utils.date_format(date_format, args[0]) + datetime.timedelta(1)
            args_str = args[0]
        else:
            for arg in args:
                if arg in months:
                    arg == months[arg]
                    break
            to_date = dutils.utils.date_format(date_format, " ".join(args)) + datetime.timedelta(1)
            args_str = " ".join(args)
        current_date = datetime.datetime.now()
        time_delta = to_date - current_date

        day_string = "days" if time_delta.days != 1 else "day"
        weeks = int(time_delta.days / 7)
        week_string = "weeks" if weeks != 1 else "week"
        days = time_delta.days % 7

        if time_delta.days == 0:
            await ctx.send("That's today!")
        if time_delta.days < 0:
            if unit is None or unit == "days":
                await ctx.send(f"{abs(time_delta.days)} {day_string} since {args_str}")
            else:
                day_string = "day" if days == 1 else "days"
                await ctx.send(f"It has been {weeks} {week_string} and {days} {day_string} since {args_str}")
        else:
            if unit is None or unit == "days":
                await ctx.send(f"{time_delta.days} {day_string} until {args_str}.")
            else:
                day_string = "day" if days == 1 else "days"
                await ctx.send(f"You have {weeks} {week_string} and {days} {day_string} until {args_str}.")

    @commands.command(description="how fucked you are!", hidden=True)
    async def howFucked(self, ctx, wage=0, hours_working=0, days_to_earn=0, amount_wanted=0):
        """Returns how fucked you are."""
        weekly_wage = wage * hours_working
        weeks_to_earn = days_to_earn / 7
        amount_earned = weekly_wage * weeks_to_earn
        if amount_earned < amount_wanted:
            await ctx.send(f"You're fucked! \nWW: {weekly_wage}\nWTE: {weeks_to_earn}\nAE: {amount_earned}")
        else:
            await ctx.send(
                f"Surprisingly, you might be okay? \nWW: {weekly_wage}\nWTE: {weeks_to_earn}\nAE: {amount_earned}")


def setup(bot):
    # bot.remove_command("help")
    bot.add_cog(Commands(bot))

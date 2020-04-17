import discord
import typing
from discord.ext import commands
from EastSql import AdminRow, OptionsRow


class AdminCommands(commands.Cog):
    """
    Designed for administrator use.
    If there isn't an assigned list of admins, defaults to anyone with admin privileges.
    """
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild.id is None:
            return True
        if ctx.author.id in ctx.bot.DEV_IDS:
            return True
        if ctx.author.id == ctx.guild.owner.id:
            return True

        admin = self.bot.database.get_admin(ctx.guild.id, ctx.author.id)

        if admin is not None:
            return True

        if admin is None and ctx.author.guild_permissions.administrator:
            return True

        return False

    @commands.group(description = "Admin related commands.", invoke_without_command = True)
    async def admins(self, ctx):
        """Admin related commands: list/show, add, remove. ``&admins [command] [command parameter]``"""
        await self._adm_show(ctx)

    @admins.command(name = "show", aliases = ["list"], description = "Shows the admins on the guild list.")
    @commands.guild_only()
    async def _adm_show(self, ctx):
        """Shows a list of admins in the current guild. ``&options show`` or ``&options list``"""
        db_admin = self.bot.database.get_admins(ctx.guild.id)

        if db_admin is not None:

            admins = "```The admins are: \n"

            for admin in db_admin:
                admin_user = ctx.bot.get_user(int(admin.user_id))
                admins += f"{admin_user.name}#{str(admin_user.discriminator)}\n"

            await ctx.send(admins + "```")
        else:
            await ctx.send("This server does not appear to have any registered admins, sorry.")

    @admins.command(name = "add", description = "Adds an admin to the guild list.")
    @commands.guild_only()
    async def _adm_add(self, ctx, user: discord.User):
        """Removes an admin from the guild list. ``&admins add @[admin]``"""
        admin = AdminRow(ctx.guild.id, user.id)
        db_admin = self.bot.database.get_admins(ctx.guild.id)
        print(admin in db_admin)
        if admin in db_admin:
            await ctx.send(user.mention + " is already an administrator.")
        else:
            self.bot.database.insert_item(admin)

            await ctx.send(user.mention + " added as an administrator!")

    @admins.command(name = "remove", description = "Removes an admin from the guild list.")
    @commands.guild_only()
    async def _adm_remove(self, ctx, user: discord.User):
        """Removes an admin from the guild list. ``&admins remove @[admin]``"""
        try:
            self.bot.database.remove_rows(AdminRow, guild_id = f"'{ctx.guild.id}'", user_id = f"'{user.id}'")
            await ctx.send(f"{user.mention} successfully removed!")
        except:
            await ctx.send(f"{user.mention} is either not an admin or does not exist.")

    @commands.group(description = "Guild options and related commands.", invoke_without_command = True)
    @commands.guild_only()
    async def options(self, ctx):
        """Guild options and related commandas (show/list, set, default.)"""
        await self._opt_show(ctx)

    @options.command(name = "show", aliases = ["list"], description = "Shows a list of options.")
    @commands.guild_only()
    async def _opt_show(self, ctx):
        """Reveals a list of options. Can be called with either ``&options show`` or ``&options list``."""
        options = self.bot.database.get_item(OptionsRow, guild_id = f"'{ctx.guild.id}'")

        embed = discord.Embed(title = "Options", color = 0xff0000)

        for opt in options:
            if opt != "guild_id":
                embed.add_field(name = opt, value = getattr(options, opt), inline = False)

        await ctx.send(embed = embed)

    @options.command(name = "set", description = "Sets an option to a new value.")
    @commands.guild_only()
    async def _opt_set(self, ctx, param: str, arg: typing.Union[int, bool, str]):
        """Sets a specific option to a new value. ``&options set [option] [value]``."""
        param = param.lower()
        options = self.bot.database.get_item(OptionsRow, guild_id = f"'{ctx.guild.id}'")
        try:
            if isinstance(arg, str):
                setattr(options, param, f"{arg}")
            else:
                setattr(options, param, arg)

            self.bot.database.update_item(options, guild_id = f"'{ctx.guild.id}'")

            await ctx.send(f"{param} set to {arg}.")
        except Exception as e:
            print(f"OPT SET: {e}")

    @options.command(name = "default", description = "Returns all options to the default.")
    @commands.guild_only()
    async def _opt_default(self, ctx):
        """Sets all options back to default. Sets:
        ``show_admins`` to True
        ``time_zone`` to UTC
        ``military_time`` to False
        ``Prefix`` to &
        """
        opt_defaults = OptionsRow(f"{ctx.guild.id}", True, "UTC", False, "&", 100)
        try:
            self.bot.database.update_item(opt_defaults, guild_id = f"'{ctx.guild.id}'")
        except Exception as e:
            self.bot.database.insert_item(opt_defaults)

        await ctx.send("All options set to default, including the prefix.")

    @commands.command(description = "Removes x amount of messages from the channel.")
    @commands.guild_only()
    async def purge(self, ctx, lim):
        await ctx.channel.purge(limit = int(lim))


def setup(bot):
    bot.add_cog(AdminCommands(bot))
import discord
import DiscordUtils as dutils
import typing
import time_zone
from discord.ext import commands
import json
import psycopg2

class AdminCommands(commands.Cog): 
    """Designed for administrator use. If there isn't an assigned list of admins, defaults to anyone with admin privileges."""
    def __init__(self, bot): 
        self.bot = bot
    
    #todo: write add_admin command tomorrow
    def cog_check(self, ctx): 
        try:
            self.bot.db.execute("""
            SELECT user_id FROM east_schema.admins
            WHERE guild_id = %s""", 
                (str(ctx.guild.id),))
            db_admin = [r[0] for r in self.bot.db.fetchall()]
        except Exception: 
            print("DB importation error.")
            db_admin = ""
        
        if ctx.guild.id is None: 
            return True
        if ctx.author.id in ctx.bot.DEV_IDS:
            return True
        if ctx.author.id == ctx.guild.owner.id: 
            return True
        
        if db_admin is not None:
            db_admin = db_admin.split(",")
            if str(ctx.author.id) in db_admin: 
                return True

        if db_admin is None and ctx.author.guild_permissions.administrator:
            return True

    @commands.group(description = "Admin related commands.")
    async def admins(self, ctx): 
        """Admin related commands: list/show, add, remove. ``&admins [command] [command parameter]``"""
        if ctx.invoked_subcommand is None: 
            await ctx.send("Options are ``list``/``show``, ``add``, and ``remove``.")
    
    @admins.command(name = "show", aliases = ["list"], description = "Shows the admins on the guild list.")
    @commands.guild_only() 
    async def _adm_show(self, ctx):
        """Shows a list of admins in the current guild. ``&options show`` or ``&options list``"""
        self.bot.db.execute("""
        SELECT user_id FROM east_schema.admins
        WHERE guild_id = %s""", 
            (str(ctx.guild.id),))
        db_admin = [r[0] for r in self.bot.db.fetchall()]
        
        if len(db_admin) != 0:

            admins = "```The admins are: \n"

            for admin_id in db_admin: 
                admin_user = ctx.bot.get_user(int(admin_id))
                admins += (f"{admin_user.name}#{str(admin_user.discriminator)}\n")
            
            await ctx.send(admins + "```")
        else: 
            await ctx.send("This server does not appear to have any registered admins, sorry.")
        
    @admins.command(name = "add", description = "Adds an admin to the guild list.")
    @commands.guild_only()
    async def _adm_add(self, ctx, user: discord.User): 
        """Removes an admin from the guild list. ``&admins add @[admin]``"""
        self.bot.db.execute("""
        SELECT user_id FROM east_schema.admins
        WHERE guild_id = %s""", 
            (str(ctx.guild.id),))
        db_admin = self.bot.db.fetchall()

        if str(user.id) in db_admin: 
            await ctx.send(user.mention + " is already an administrator.")
        else: 
            self.bot.db.execute("""
                INSERT INTO east_schema.admins (guild_id, user_id)
                VALUES (%s, %s)
                """,
                    (str(ctx.guild.id), str(user.id)))
                    
            await ctx.send(user.mention + " added as an administrator!") 

    @admins.command(name = "remove", description = "Removes an admin from the guild list.")
    @commands.guild_only()
    async def _adm_remove(self, ctx, user: discord.User):
        """Removes an admin from the guild list. ``&admins remove @[admin]``"""
        try: 
            self.bot.db.execute("""
            DELETE FROM east_schema.admins
            WHERE guild_id = %s AND user_id = %s""", 
                (str(ctx.guild.id), str(user.id)))
            await ctx.send(f"{user.mention} successfully removed!")
        except: 
            await ctx.send(f"{user.mention} is either not an admin or does not exist.")


    @commands.group(description = "Guild options and related commands.")
    @commands.guild_only()
    async def options(self, ctx):
        """Guild options and related commandas (show/list, set, default.)"""
        if ctx.invoked_subcommand is None: 
            await ctx.send("Options are ``show``/``list``, ``set``, and ``default.``")
    
    @options.command(name = "show", aliases = ["list"], description = "Shows a list of options.")
    @commands.guild_only()
    async def _opt_show(self, ctx): 
        """Reveals a list of options. Can be called with either ``&options show`` or ``&options list``."""
        db = self.bot.db
        db.execute("SELECT json_object_keys(to_json((SELECT t FROM options t LIMIT 1)));")
        opt_list = [r[0] for r in db.fetchall()]
        db.execute("SELECT * FROM east_schema.options WHERE guild_id = %s",
            (str(ctx.guild.id),))
        response_list = list(db.fetchone())

        #Get the index of each item we want to remove (in case more rows
        #are added or removed) and remove them for each of the lists. Due 
        #to getter method, values should correspond. 
        response_list.pop(opt_list.index("guild_id"))
        opt_list.pop(opt_list.index("guild_id"))

        embed = discord.Embed(title = "Options", color = 0xff0000)
        for i, option in enumerate(opt_list):
            embed.add_field(name = option, value = response_list[i], inline = False)
        
        await ctx.send(embed = embed)

    @options.command(name = "set", description = "Sets an option to a new value.")
    @commands.guild_only()
    async def _opt_set(self, ctx, param: str, arg: typing.Union[int, str]): 
        """Sets a specific option to a new value. ``&options set [option] [value]``."""
        param = param.lower()

        opt_list = ctx.bot.OPTIONS_LIST
        if param in opt_list.keys():
            if(isinstance(arg, opt_list[param])):
                self.bot.db.execute("""
                UPDATE east_schema.options SET {} = %s 
                WHERE guild_id = %s;"""
                    .format(param),
                    (arg, str(ctx.guild.id)))
                await ctx.send(f"{param} set to {arg}.")
            else: 
                await ctx.send(f"{arg} is not the right type of argument for {param}.")
        else: 
            await ctx.send(f"{param} is not an option. To see options, type &options show.")
        
        # with open("data_storage.json", "w") as file:
        #     json.dump(self.bot.data, file)
    
    @options.command(name = "default", description = "Returns all options to the default.")
    @commands.guild_only()
    async def _opt_default(self, ctx): 
        """Sets all options back to default. Sets:
        ``show_admins`` to True
        ``time_zone`` to UTC
        ``military_time`` to False
        ``Prefix`` to &
        """
        self.bot.db.execute("""
        SELECT * FROM east_schema.options 
        WHERE guild_id = %s
        """, 
           (str(ctx.guild.id),)) 

        if self.bot.db.fetchone() is None:
            self.bot.db.execute("""
            INSERT INTO east_schema.options (guild_id, show_admins, time_zone, military_time, prefix, scoreboard_pl) 
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
                (str(ctx.guild.id), True, "UTC", False, "&", 100))
        else: 
            self.bot.db.execute("""
            UPDATE east_schema.options 
            SET show_admins = %s, time_zone = %s, military_time = %s, scoreboard_pl = %s, prefix = %s
            WHERE guild_id = %s;""",
                (True, "UTC", False, 100, "&", str(ctx.guild.id)))
        await ctx.send("All options set to default, including the prefix.")            
    
    @commands.command(description = "Removes x amount of messages from the channel.")
    @commands.guild_only()
    async def purge(self, ctx, lim): 
        await ctx.channel.purge(limit = int(lim))

def setup(bot): 
    bot.add_cog(AdminCommands(bot))
import sys
sys.path.append('C:\\Dev\\SedezCompendium')

import sedezcompendium.discordtools as dtutils
import discord
import tokens_and_pswds as tap
import EastSql as sql

TOKEN = tap.get_discord_token()


class East (discord.ext.commands.Bot):

    def __init__(self, **kwargs):
        if kwargs.get("help_command") is None: 
            kwargs["help_command"] = dtutils.utils.EastHelpCommand()

        super().__init__(**kwargs)

    database = sql.EastDatabase("eastdb", "localhost", 5432, "EastBot", tap.get_db_pass(), "east_schema", True)

    SPLIT_CHAR = ','
    LOAD_COGS = ['commands', 'dev_commands', 'admin_commands', 'joke_commands']
    DEV_IDS = [199856712860041216, 101091070904897536]
    OPTIONS_LIST = {
        "show_admins" : bool, 
        "time_zone" : dtutils.timezone.TimeZone,
        "military_time" : bool,
        "prefix" :   str
    }

    # BOT LOGS
    async def on_ready(self): 
        print('Logged in as ')  
        print(bot.user.name)
        print(bot.user.id)
        print('-----')
    
    async def on_guild_join(self, guild):
        opt_row = sql.OptionsRow(f"'{guild.id}'", True, "UTC", False, "&", 100)
        self.database.insert_item(opt_row)

    async def on_guild_remove(self, guild):
        self.database.remove_item(sql.OptionsRow, guild_id = f"'{guild.id}'")
        self.database.remove_item(sql.AdminRow, guild_id = f"'{guild.id}'")
    
    async def process_commands(self, message): 
        if message.author.bot and not (message.author.id == 199965612691292160):
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)


def get_prefix(self, ctx):
    options_row = self.database.get_item(sql.OptionsRow, guild_id = f"'{ctx.guild.id}'")
    prefix = getattr(options_row, "prefix")
    if prefix is not None:
        return prefix
    else:
        return "&"


bot = East(command_prefix = get_prefix)

for cog in bot.LOAD_COGS:
    bot.load_extension("cogs." + cog)

bot.run(TOKEN)
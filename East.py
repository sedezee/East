import sys
sys.path.append('C:\\Dev\\python\\SedezCompendium')

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

    # BOT LOGS
    async def on_ready(self): 
        print('Logged in as ')  
        print(bot.user.name)
        print(bot.user.id)
        print('-----')
    
    async def on_guild_join(self, guild):
        opt_row = sql.OptionsRow(f"'{guild.id}'", True, "'UTC'", False, "'&'", 100, "MM/DD/YY", False, False)
        self.database.insert_item(opt_row)

    async def on_guild_remove(self, guild):
        #TODO: add the rest
        self.database.remove_rows(sql.OptionsRow, guild_id = f"'{guild.id}'")
        self.database.remove_rows(sql.AdminRow, guild_id = f"'{guild.id}'")

    async def process_commands(self, message): 
        if message.author.bot and not (message.author.id == 199965612691292160):
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)


def get_prefix(self, ctx):
    options_row = self.database.get_item(sql.OptionsRow, guild_id = f"'{ctx.guild.id}'")
    try:
        return getattr(options_row, "prefix")
    except AttributeError:
        return "&"


bot = East(command_prefix = get_prefix)

for cog in bot.LOAD_COGS:
    bot.load_extension("cogs." + cog)

bot.run(TOKEN)
import discord
from discord.ext import commands
import DiscordUtils as dutils
import tokens_and_pswds as tap

import random
import time_zone

import json
import psycopg2

TOKEN = tap.getDiscordToken()


class East (commands.Bot):

    def __init__(self, **kwargs):
        if kwargs.get("help_command") is None: 
            kwargs["help_command"] = dutils.EastHelpCommand()

        super().__init__(**kwargs)

    with open ("data_storage.json", "r") as file: 
        data = json.load(file)

    conn = psycopg2.connect(f"dbname = eastdb user=EastBot password = {tap.getDBPass()}")
    conn.set_session(autocommit = True)
    db = conn.cursor()

    SPLIT_CHAR = ','
    LOAD_COGS = ['commands', 'dev_commands', 'admin_commands', 'joke_commands']
    DEV_IDS = [199856712860041216, 101091070904897536]
    OPTIONS_LIST = {
        "show_admins" : bool, 
        "time_zone" : time_zone.TimeZone,
        "military_time" : bool,
        "prefix" :   str
    }

    #BOT LOGS
    async def on_ready(self): 
        print('Logged in as ')  
        print(bot.user.name)
        print(bot.user.id)
        print('-----')
    
    async def on_guild_join(self, guild):
        self.db.execute("""
        INSERT INTO options (guild_id, show_admins, time_zone, military_time, prefix, scoreboard_pl) 
        VALUES (%s, %s, %s, %s, %s, %s);
        """,
            (str(guild.id), True, "UTC", False, "&", 100))
    
    async def on_guild_remove(self, guild): 
        self.db.execute("DELETE FROM options WHERE guild_id = %s;", 
            (str(guild.id),))
        self.db.execute("DELETE FROM scoreboard WHERE guild_id = %s", 
            (str(guild.id),))
    
    async def process_commands(self, message): 
        if message.author.bot and not (message.author.id == 199965612691292160):
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)


def getPrefix(self, ctx): 
    self.db.execute("""
    SELECT prefix FROM options
    WHERE guild_id = %s;
    """, 
        (str(ctx.guild.id),))
    
    return self.db.fetchone()

bot = East(command_prefix = getPrefix)

for cog in bot.LOAD_COGS:
    bot.load_extension("cogs." + cog)

bot.run(TOKEN)
import discord
from discord.ext import commands
import random
import time_zone
import json
import re

TOKEN = ""


class East (commands.Bot):

    with open ("data_storage.json", "r") as file: 
        data = json.load(file)

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
        bot.data[str(guild.id)] = {}
        bot.data[str(guild.id)]["admin_ids"] = []
        bot.data[str(guild.id)]["options"] = {}
        bot.data[str(guild.id)]["options"]["show_admins"] = True
        bot.data[str(guild.id)]["options"]["time_zone"] = "UTC"
        bot.data[str(guild.id)]["options"]["military_time"] = False
        bot.data[str(guild.id)]["options"]["prefix"] = "&"
        with open("data_storage.json", "w") as file: 
            json.dump(bot.data, file)
            data = json.load(file)
    
    async def process_commands(self, message): 
        if message.author.bot and not (message.author.id == 199965612691292160):
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)


def getPrefix(self, ctx): 
    return bot.data[str(ctx.guild.id)]["options"]["prefix"]

bot = East(command_prefix = getPrefix)

for cog in bot.LOAD_COGS:
    bot.load_extension("cogs." + cog)

bot.run(TOKEN)
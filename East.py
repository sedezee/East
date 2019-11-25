import discord
from discord.ext import commands
import random
import time_zone
import json
import re

TOKEN = "NjQxMDkzMjQ2MDkyNzA1ODE0.XcDXtw.LsC7erHW4CDPYccaj0FVq16Y-oY"

with open ("data_storage.json", "r") as file: 
    data = json.load(file)

class East (commands.Bot):

    SPLIT_CHAR = ','
    LOAD_COGS = ['cogs.commands', 'cogs.dev_commands', 'cogs.admin_commands']
    DEV_IDS = [199856712860041216, 101091070904897536]
    OPTIONS_LIST = {
        "show_admins" : bool, 
        "time_zone" : time_zone.TimeZone,
        "military_time" : bool,
        "prefix" : str
    }

    #BOT LOGS
    async def on_ready(self): 
        print('Logged in as ')
        print(bot.user.name)
        print(bot.user.id)
        print('-----')
    
    async def on_guild_join(self, guild):
        data[str(guild.id)] = {}
        data[str(guild.id)]["admin_ids"] = []
        data[str(guild.id)]["options"] = {}
        data[str(guild.id)]["options"]["show_admins"] = True
        data[str(guild.id)]["options"]["time_zone"] = "UTC"
        data[str(guild.id)]["options"]["military_time"] = False
        data[str(guild.id)]["options"]["prefix"] = "&"
        with open("data_storage.json", "w") as file: 
            json.dump(data, file)

        
def getPrefix(self, ctx): 
    with open ("data_storage.json", "r") as file: 
        data = json.load(file)
    return data[str(ctx.guild.id)]["options"]["prefix"]

bot = East(command_prefix = getPrefix)

for cog in bot.LOAD_COGS:
    bot.load_extension(cog)

bot.run(TOKEN)
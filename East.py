import discord
from discord.ext import commands
import random
import json
import re

TOKEN = "NjQxMDkzMjQ2MDkyNzA1ODE0.XcDXtw.LsC7erHW4CDPYccaj0FVq16Y-oY"

with open ("data_storage.json", "r") as file: 
    data = json.load(file)

class East (commands.Bot):

    SPLIT_CHAR = ','
    LOAD_COGS = ['cogs.commands', 'cogs.dev_commands', 'cogs.admin_commands']
    DEV_IDS = [199856712860041216, 101091070904897536]
    PERMS_LIST = ["show_admins"]
    #BOT LOGS
    async def on_ready(self): 
        print('Logged in as ')
        print(bot.user.name)
        print(bot.user.id)
        print('-----')
    
    async def on_guild_join(self, guild):
        data[str(guild.id)] = {}
        data[str(guild.id)]["show_admins"] = True
        with open("data_storage.json", "w") as file: 
            json.dump(data, file)

        

bot = East("&")

for cog in bot.LOAD_COGS:
    bot.load_extension(cog)

bot.run(TOKEN)
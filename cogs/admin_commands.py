import discord
from discord.ext import commands
import json

with open ("data_storage.json", "r") as file: 
    data = json.load(file)


class AdminCommands(commands.Cog): 
    """Designed for administrator use. If there isn't an assigned list of admins, defaults to anyone with admin privileges."""
    def __init__(self, bot): 
        self.bot = bot
    
    #todo: write add_admin command tomorrow
    def cog_check(self, ctx): 
        dataIndex = data[str(ctx.guild.id)]["admin_ids"]
        
        if ctx.guild.id is None: 
            return True
        if ctx.author.id in ctx.bot.DEV_IDS:
            return True
        if ctx.author.id == ctx.guild.owner.id: 
            return True
        
        if ctx.author.id in dataIndex: 
            return True

        if len(dataIndex) and ctx.author.guild_permissions.administrator:
            return True

    @commands.command(description = "Adds an admin to the guild list.")
    @commands.guild_only()
    async def addAdmin(self, ctx, user: discord.User):
        dataIndex = data[str(ctx.guild.id)]["admin_ids"]
        
        try:
            if ctx.guild.id is None:
                await ctx.send("You're not in a guild.")       
            else:  
                if data[str(ctx.guild.id)].get("admin_ids") is None or len(dataIndex): 
                    dataIndex = [user.id]
                    await ctx.send(user.mention + " added as an administrator!")
                elif user.id in dataIndex: 
                    await ctx.send(user.mention + " is already an administrator.")
                elif not user.id in dataIndex:
                    dataIndex.append(user.id)
                    await ctx.send(user.mention + " added as an administrator!") 
            with open("data_storage.json", "w") as file: 
                json.dump(data, file)
        except: 
            await ctx.send("Please submit a valid admin name.")
    
    @commands.command(aliases = ["rmAdmin"], description = "Removes an admin from the guild list.")
    @commands.guild_only()
    async def removeAdmin(self, ctx, user: discord.User):
        #remove admin and add admin use the same search functionality. streamline it.   
        dataIndex = data[str(ctx.guild.id)]["admin_ids"]
        try: 
            if ctx.guild.id is None: 
                await ctx.send("You're not in a guild.")
            else: 
                if data[str(ctx.guild.id)].get("admin_ids") is None or len(dataIndex) == 0: 
                    await ctx.send("There are no admins to remove.")
                elif not user.id in dataIndex:
                    await ctx.send(user.mention + " is not an administrator.")
                elif user.id in dataIndex: 
                    await ctx.send(user.mention + " removed.")
                    dataIndex.remove(user.id)
            with open("data_storage.json", "w") as file: 
                json.dump(data, file)
        except: 
            await ctx.send("Please submit a valid admin name.")
    
    @commands.command(description = "Sets the permissions for a guild.")
    @commands.guild_only() 
    async def setPerms(self, ctx, param, arg:bool): 
        dataIndex = data[str(ctx.guild.id)]
        try:
            if param in dataIndex: 
                dataIndex[param] = arg
                await ctx.send(param + " set to " + str(arg))
            else: 
                await ctx.send("Please enter a valid permission name.")
            with open("data_storage.json", "w") as file: 
                json.dump(data, file)
        except: 
            await ctx.send("Please submit a valid permission name and a true/false variable.")
    
    @commands.command(description = "Shows the permissions for a guild.")
    @commands.guild_only()
    async def showPerms(self, ctx):
        perms_out = ""
        for item in ctx.bot.PERMS_LIST: 
            if (item in data[str(ctx.guild.id)]):
                perms_out += (str(item) + " : " + str(data[str(ctx.guild.id)][item]) + "\n")
        await ctx.send("```" + perms_out + "```")

    @commands.command(description = "Removes x amount of messages from the channel.")
    @commands.guild_only()
    async def purge(self, ctx, lim): 
        await ctx.channel.purge(limit = int(lim))

def setup(bot): 
    bot.add_cog(AdminCommands(bot))
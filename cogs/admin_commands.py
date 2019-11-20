import discord
import DiscordUtils as dutils
import typing
import time_zone
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

        if len(dataIndex) == 0 and ctx.author.guild_permissions.administrator:
            return True

    @commands.group()
    async def admins(self, ctx): 
        if ctx.invoked_subcommand is None: 
            await ctx.send("Options are ``list``/``show``, ``add``, and ``remove``.")
    
    @admins.command(aliases = ["list", "show"])
    @commands.guild_only()
    async def _adm_show(self, ctx):
        dataIndex = data[str(ctx.guild.id)]["admin_ids"]
        admins = "```The admins are: \n"

        for item in dataIndex: 
            admin_user = ctx.bot.get_user(item)
            admins += (f"{admin_user.name}#{str(admin_user.discriminator)}\n")
        
        await ctx.send(admins + "```")
        
    @admins.command(name = "add")
    @commands.guild_only()
    async def _adm_add(self, ctx, user: discord.User): 
        dataIndex = data[str(ctx.guild.id)]["admin_ids"]
        try:
            if user.id in dataIndex: 
                await ctx.send(user.mention + " is already an administrator.")
            elif not user.id in dataIndex:
                dataIndex.append(user.id)
                await ctx.send(user.mention + " added as an administrator!") 
            with open("data_storage.json", "w") as file: 
                json.dump(data, file)
        except: 
            await ctx.send("Please submit a valid admin name.")

    @admins.command(name = "remove")
    @commands.guild_only()
    async def _adm_remove(self, ctx, user: discord.User):
        #remove admin and add admin use the same search functionality. streamline it.   
        dataIndex = data[str(ctx.guild.id)]["admin_ids"]
        try: 
            if not user.id in dataIndex:
                await ctx.send(user.mention + " is not an administrator.")
            elif user.id in dataIndex: 
                await ctx.send(user.mention + " removed.")
                dataIndex.remove(user.id)
            with open("data_storage.json", "w") as file: 
                json.dump(data, file)
        except: 
            await ctx.send("Please submit a valid admin name.")

    @commands.group()
    async def options(self, ctx):
        if ctx.invoked_subcommand is None: 
            await ctx.send("Options are ``show``/``list``, ``set``, and ``default.``")
    
    @options.command(name = "show", aliases = ["list"])
    async def _opt_show(self, ctx): 
        opt_out = ""
        for item in ctx.bot.OPTIONS_LIST.keys():
            opt_out += ("{0} : {1} \n"
                .format(str(item), str(data[str(ctx.guild.id)]["options"][item])))
        await ctx.send(f"```{opt_out}```")

    @options.command(name = "set")
    async def _opt_set(self, ctx, param, arg: typing.Union[time_zone.TimeZone, int, str]): 
        param = param.lower()
        opt_list = ctx.bot.OPTIONS_LIST
        if param in opt_list.keys():
            if(isinstance(arg, opt_list[param])):  
                data[str(ctx.guild.id)]["options"][param] = arg
                await ctx.send(f"{param} set to {arg}.")
            else: 
                await ctx.send(f"{arg} is not the right type of argument for {param}.")
        else: 
            await ctx.send(f"{param} is not an option. To see options, type &options show.")
        
        with open("data_storage.json", "w") as file: 
            json.dump(data, file)
    
    @options.command(name = "default")
    async def _opt_default(self, ctx): 
        data[str(ctx.guild.id)]["options"]["show_admins"] = True
        data[str(ctx.guild.id)]["options"]["time_zone"] = "UTC"
        data[str(ctx.guild.id)]["options"]["military_time"] = False
        await ctx.send("All options set to default.")            
    
    @commands.command(description = "Removes x amount of messages from the channel.")
    async def purge(self, ctx, lim): 
        await ctx.channel.purge(limit = int(lim))

def setup(bot): 
    bot.add_cog(AdminCommands(bot))
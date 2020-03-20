import discord
from discord.ext import commands
import asyncio

class JokeCommands(commands.Cog):
    """These commands are just for fun. Once the main purpose of East, now only a few favorites remain."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ['East,'], description = "East will do a favor, but only for a certain bot...")
    async def favor(self, ctx, *, args = "no"):
        """East performs a favor for a certain someone, and ONLY that someone."""
        if ctx.author.id != 199965612691292160:
            await ctx.send("Excuse me?")
            return 
         
        await asyncio.sleep(1)
        async with ctx.typing(): 
            await asyncio.sleep(1)
            await ctx.send("Only if you tear through mine first ;)")

    @commands.command(aliases = ["hello", "sayHelloTo"], description = "East will say hello! Certain key words may invoke a unique response.")
    async def sayHello(self, ctx, recipient = None):
        """East says hello. Certain unique keywords may provoke a different response, however..."""
        talos = ctx.guild.get_member(199965612691292160)
        if recipient == "Talos" and talos or talos.status != discord.Status.online:
            await ctx.send("^Hello there...")
            await asyncio.sleep(1)
            async with ctx.typing():
                await asyncio.sleep(1)
                await ctx.send("I hope you're doing well!")
        else: 
            await ctx.send(f"Hello {ctx.author.name}!")

def setup(bot):
    bot.add_cog(JokeCommands(bot))
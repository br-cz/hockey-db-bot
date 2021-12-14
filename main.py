import discord
from discord import guild

bot = discord.Bot()

@bot.slash_command(name="greet", description="get the bot to greet yourself or someone")
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")
    
@bot.slash_command(guild_ids=[920041129741791294], description="get player queries")#name="get player queries", description="used to see all the available player queries")
async def gpq(ctx):
    await ctx.respond("You've chosen to see player queries")
    
@bot.slash_command(guild_ids=[920041129741791294], description="get coach queries")#name="get player queries", description="used to see all the available player queries")
async def gcq(ctx):
    await ctx.respond("You've chosen to see coach queries")
    
@bot.slash_command(guild_ids=[920041129741791294], description="Find the names of all players who have played in at least x different teams")#name="get player queries", description="used to see all the available player queries")
async def dt(ctx, numteam: int):
    numteam = numteam
    await ctx.respond(f"Find the names of all players who have played in at least {numteam} different teams")
    
# async def gcq(ctx):
#     await ctx.respond("You've chose to see coach queries")
    
# @bot.slash_command(name="restart")
# async def restart(ctx):
#     await ctx.respond("Restarting myself!")
#     await bot.close()


bot.run("OTIwMDQ1MTYwMjI0NjU3NDM4.Ybeo0w.XPlqvacAYT2rHPm7OuoKj6Zp1SM")

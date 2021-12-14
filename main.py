import discord

bot = discord.Bot()

@bot.slash_command()
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")


bot.run("OTIwMDQ1MTYwMjI0NjU3NDM4.Ybeo0w.XPlqvacAYT2rHPm7OuoKj6Zp1SM")


import discord
from discord import guild
from discord import embeds
from discord import emoji
# from discord.components import Button
# from discord.ui.button import button
# from discord.ui.view import View

bot = discord.Bot()

class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="but", style=discord.ButtonStyle.url, url="google.com"))
        
        
class Start(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Github Repo", style=discord.ButtonStyle.url, url="https://github.com/br-cz/hockey-db-bot"))
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="Let's get started!", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        self.stop()
  
@bot.slash_command(guild_ids=[920041129741791294])
async def start(ctx):    
    view = Start()
    
    embed = discord.Embed(
        title = "Welcome!",
        description="I'm Sidney Crosbot, feel free to ask me anything about hockey"
    )
    
    await ctx.respond(embed=embed, view=view)

@bot.slash_command(name="greet", description="get the bot to greet yourself or someone")
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")
    
@bot.slash_command(guild_ids=[920041129741791294], description="get player queries")
async def gpq(ctx):
    await ctx.respond("You've chosen to see player queries")
    
@bot.slash_command(guild_ids=[920041129741791294], description="get coach queries")
async def gcq(ctx):
    await ctx.respond("You've chosen to see coach queries")
    
@bot.slash_command(guild_ids=[920041129741791294], description="Find the names of all players who have played in at least x different teams")#name="get player queries", description="used to see all the available player queries")
async def dt(ctx, numteam: int):
    numteam = numteam
    await ctx.respond(f"Find the names of all players who have played in at least {numteam} different teams")
    
bot.run("OTIwMDQ1MTYwMjI0NjU3NDM4.Ybeo0w.XPlqvacAYT2rHPm7OuoKj6Zp1SM")

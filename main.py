import discord
from discord import guild
from discord import embeds
from discord import emoji
from discord.colour import CT
# from discord.components import Button
# from discord.ui.button import button
# from discord.ui.view import View

bot = discord.Bot()

#Class storing the view of the different entities
class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Teams", style=discord.ButtonStyle.primary))
        self.add_item(discord.ui.Button(label="Coaches", style=discord.ButtonStyle.primary))
        self.add_item(discord.ui.Button(label="Players", style=discord.ButtonStyle.primary))
        self.add_item(discord.ui.Button(label="Games", style=discord.ButtonStyle.primary))
        self.add_item(discord.ui.Button(label="Person", style=discord.ButtonStyle.primary))    
        
        
class Start(discord.ui.View):
    def __init__(self):
        super().__init__()
        #github repo button
        self.add_item(discord.ui.Button(label="Github Repo", style=discord.ButtonStyle.url, url="https://github.com/br-cz/hockey-db-bot"))
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    @discord.ui.button(label="Let's get started!", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        #await interaction.response.send_message("Confirming", ephemeral=True)
        embed = discord.Embed(
            title="Which entity do you wish to see the table and queries of?"
        )
        embed.add_field(name="Teams", value="Field Value", inline="False")
        embed.add_field(name="Coaches", value="Coaches Value", inline="False")
        embed.add_field(name="Players", value="Players Value", inline="False")
        embed.add_field(name="Games", value="Games Value", inline="False")
        embed.add_field(name="Person", value="Person Value", inline="False")
        await interaction.response.edit_message(view=ButtonView(), embed=embed)
        
        
    
@bot.slash_command(guild_ids=[920041129741791294])
async def start(ctx):   
    clicked = False 
    view = Start()
    
    embed = discord.Embed(
        title = "Welcome!",
        description="I'm Sidney Crosbot, feel free to ask me anything about hockey"
    )
    
    await ctx.respond(embed=embed, view=view)
    await view.wait()
   
   # await ctx.respond(embed=embed,view=view)
   
  
















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

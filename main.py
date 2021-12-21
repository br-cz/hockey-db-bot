import discord

bot = discord.Bot(intents=discord.Intents().all())
 
#Welcome message   
@bot.event
async def on_member_join(member):
    guild = member.guild
    welcomeembed = discord.Embed(timestamp = member.joined_at)
    welcomeembed.set_author(name=f"{member.display_name}", icon_url = f'{member.display_avatar}')
    welcomeembed.set_thumbnail(url="https://media.discordapp.net/attachments/920041130270269473/922366383310925824/CrosbyArt.jpg")
    welcomeembed.add_field(name=f"Welcome to the `{guild}`", value='\u200b', inline=False)
    welcomeembed.add_field(name="Type /start to get started!", value='\u200b', inline=False)
    welcomeembed.set_image(url="https://media.giphy.com/media/xUPGGDNsLvqsBOhuU0/giphy.gif")
    await guild.get_channel(920041130270269473).send(embed=welcomeembed)

#Used to initiate the main menu
@bot.slash_command(guild_ids=[920041129741791294])
async def start(ctx):   
    view = Start()#The start menu
    
    embed = discord.Embed(
        title = "Welcome!",
        description="I'm Sidney Crosbot, feel free to ask me anything about hockey."
    )
    
    await ctx.respond(embed=embed, view=view)
    
    
#Subclass of View used to handle the main menu
class Start(discord.ui.View):
    def __init__(self):
        super().__init__()
        #github repo button
        self.add_item(discord.ui.Button(label="Github Repo", style=discord.ButtonStyle.url, url="https://github.com/br-cz/hockey-db-bot"))
        self.value = None

    #When the confirm button is pressed, show the next set of options for the user to pick from
    #Here we're showing the tables the user can pick from
    @discord.ui.button(label="Let's get started!", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Which entity do you wish to see the table and queries of?"
        )
        await interaction.response.edit_message(view=EntityButtons(), embed=embed)
        
#Subclass of View used to store the different entities in the db
class EntityButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) 
    
    #When these buttons are clicked, show the available queries according to the labeled table 
    #The following methods apparently need button, regardless if its used or not
    #Removing button gives the following error: "TypeError: EntityButtons.confirmTeam() takes 2 positional arguments but 3 were given"
    @discord.ui.button(label="Teams", style=discord.ButtonStyle.primary)
    async def confirmTeam(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Please pick the sample query you wish to see!",
            description="Type the associated slash command to get the query"
        )
        embed.add_field(name="/tc", value="This is what the query does", inline=False)
        embed.add_field(name="/tq", value="This is what the query does", inline=False)
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="Person", style=discord.ButtonStyle.primary)
    async def confirmPerson(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
          title="Please pick the sample query you wish to see!",
            description="Type the associated slash command to get the query"
        )
        embed.add_field(name="/perc", value="This is what the query does", inline=False)
        embed.add_field(name="/perq", value="This is what the query does", inline=False)
        await interaction.response.edit_message(embed=embed)
        
    @discord.ui.button(label="Coaches", style=discord.ButtonStyle.primary)
    async def confirmCoach(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
             title="Please pick the sample query you wish to see!",
            description="Type the associated slash command to get the query"
        )
        embed.add_field(name="/cc", value="This is what the query does", inline=False)
        embed.add_field(name="/cq", value="This is what the query does", inline=False)
        await interaction.response.edit_message(embed=embed)
        
    @discord.ui.button(label="Players", style=discord.ButtonStyle.primary)
    async def confirmPlayer(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
      title="Please pick the sample query you wish to see!",
            description="Type the associated slash command to get the query"
        )
        embed.add_field(name="/pc", value="This is what the query does", inline=False)
        embed.add_field(name="/pq", value="This is what the query does", inline=False)
        await interaction.response.edit_message(embed=embed)
        
    @discord.ui.button(label="Games", style=discord.ButtonStyle.primary)
    async def confirmGame(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
             title="Please pick the sample query you wish to see!",
            description="Type the associated slash command to get the query"
        )
        embed.add_field(name="/gc", value="This is what the query does", inline=False)
        embed.add_field(name="/gq", value="This is what the query does", inline=False)
        await interaction.response.edit_message(embed=embed)
        
    @discord.ui.button(label="Goals", style=discord.ButtonStyle.primary)
    async def confirmGoals(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
          title="Please pick the sample query you wish to see!",
            description="Type the associated slash command to get the query"
        )
        embed.add_field(name="/gerc", value="This is what the query does", inline=False)
        embed.add_field(name="/gerq", value="This is what the query does", inline=False)
        await interaction.response.edit_message(embed=embed)
        

#Queries for later
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
    
@bot.slash_command(guild_ids=[920041129741791294], description="Find the names of all players who have played in at least x different teams")
async def dt(ctx, numteam: int):
    numteam = numteam
    await ctx.respond(f"Find the names of all players who have played in at least {numteam} different teams")
    
    

bot.run("OTIwMDQ1MTYwMjI0NjU3NDM4.Ybeo0w.XPlqvacAYT2rHPm7OuoKj6Zp1SM")

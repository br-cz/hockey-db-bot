from bot_utils import *
from config import *
from discord.colour import CT

bot = discord.Bot(intents=discord.Intents().all())

# Welcome message	
@bot.event
async def on_member_join(member):
	guild = member.guild
	welcomeembed = discord.Embed(timestamp = member.joined_at)
	welcomeembed.set_author(name=f"{member.display_name}", icon_url = f'{member.display_avatar}')
	welcomeembed.set_thumbnail(url="https://media.discordapp.net/attachments/920041130270269473/922366383310925824/CrosbyArt.jpg")
	welcomeembed.add_field(name=f"Welcome to the `{guild}`", value='\u200b', inline=False)
	welcomeembed.add_field(name="Type /start to get started!", value='\u200b', inline=False)
	welcomeembed.set_image(url="https://media.giphy.com/media/xUPGGDNsLvqsBOhuU0/giphy.gif")
	await guild.get_channel(CHANNEL_ID).send(embed=welcomeembed)
		 
# Used to initiate the main menu
@bot.slash_command(guild_ids=[GUILD_ID], description = "View the start menu")
async def start(ctx):	
	view = Start() # The start menu
	embed = discord.Embed(title = "Welcome!", description="I'm Sidney Crosbot, feel free to ask me anything about hockey")
	await ctx.respond(embed=embed, view=view)

# Subclass of View used to handle the manin menu
class Start(discord.ui.View):
	def __init__(self):
		super().__init__()
		# github repo button
		self.add_item(discord.ui.Button(label="Github Repo", style=discord.ButtonStyle.url, url="https://github.com/br-cz/hockey-db-bot"))
		self.value = None

	#When the confirm button is pressed, show the next set of options for the user to pick from
	#Here we're showing the tables the user can pick from
	@discord.ui.button(label="Let's get started!", style=discord.ButtonStyle.green)
	async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(title="Which entity do you wish to see the table and queries of?")
		await interaction.response.edit_message(view=EntityButtons(), embed=embed)
  
#Subclass of View storing the different entities
class EntityButtons(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None) 
	
	# When these buttons are clicked, show the available queries according to the labeled table 
	''' Teams '''
	@discord.ui.button(label="Teams", style=discord.ButtonStyle.primary)
	async def confirmTeam(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(title="Here are the available queries!", description="Type the associated slash command to get the query")
		embed.add_field(name="/tt", value="Get 100 entries of Team table", inline=False)
		embed.add_field(name="/tst", value="Get 100 entries of Team_Stats table", inline=False)
		embed.add_field(name="/tunq", value="Find the teams who've signed the most players in total", inline=False)
		embed.add_field(name="/tspk", value="Find the best teams at scoring on the penalty kill in a single season", inline=False)
		embed.add_field(name="/tss", value="Find the standings for a given season", inline=False)
		embed.add_field(name="/tsf", value="Find franchise stats for a given team", inline=False)
		embed.add_field(name="/tsts", value="Find the stats for a specific team, season, or both", inline=False)
		embed.add_field(name="/tsmd", value="Find the most dominant teams of all time (most wins, least losses, OTL, and SOL)", inline=False)
		embed.add_field(name="/tmup", value="Find the teams with the largest number of unique players in one season", inline=False)
		embed.add_field(name="/tpp", value="Find all teams that a specific player has played for", inline=False)
		await interaction.response.edit_message(embed=embed)
	
	''' Coaches '''
	@discord.ui.button(label="Coaches", style=discord.ButtonStyle.primary)
	async def confirmCoach(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(title="Here are the available queries!", description="Type the associated slash command to get the query")
		embed.add_field(name="/hdt", value="Get 100 entries of Head_Coach table", inline=False)
		embed.add_field(name="/cunq", value="Find the coaches that have coached the most (unique) players while coaching over the years", inline=False)
		embed.add_field(name="/hcmt", value="Find the head coaches that have worked for the most teams", inline=False)
		embed.add_field(name="/hcos", value="List all the head coaches ordered descending by a given statistic (GP, Wins, Losses, OTL)", inline=False)
		await interaction.response.edit_message(embed=embed)
		
	''' Players '''
	@discord.ui.button(label="Players", style=discord.ButtonStyle.primary)
	async def confirmPlayer(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(title="Here are the available queries!", description="Type the associated slash command to get the query")
		embed.add_field(name="/plt", value="Get 100 entries of player table", inline=False)
		embed.add_field(name="/pxdt", value="Find the names of all players who have played in at least x different teams", inline=False)
		embed.add_field(name="/pss", value="Find the names of all players who have scored an equal number of goals, and assists over the seasons ordered by said number", inline=False)
		embed.add_field(name="/phsl", value="Find the players who had the highest stat-line for their team in a season", inline=False)
		embed.add_field(name="/psmt", value="Find the names of the players who've played for the most teams", inline=False)
		embed.add_field(name="/posl", value="Find all clutch players (players that scored a goal with 1 second left to tie the game)", inline=False)
		embed.add_field(name="/plao", value="Find all the players that have scored less across their career than Alex Ovechkin on the powerplay", inline=False)
		embed.add_field(name="/pncc", value="Find all the Hockey players and the # of coaching changes they've had while playing for 1 team", inline=False)
		embed.add_field(name="/psg", value="Find the best performing players in a season where they only played one game (with a given team)", inline=False)
		embed.add_field(name="/pfgt", value="Find the first goal scored by a specific player with a specific team", inline=False)  
		embed.add_field(name="/pmgo", value="Find the players with the most goals in one game", inline=False)  
		embed.add_field(name="/pcos", value="List all the players ordered descending by a given statistic (GP, Wins, Losses, OTL)", inline=False)
		embed.add_field(name="/phtm", value="List players with the number of games in which they scored >= 3 goals", inline=False)
		embed.add_field(name="/pbgs", value="Find the best goal scorer from a given place", inline=False)
		embed.add_field(name="/pold", value="Find the oldest active players in the NHL", inline=False)
		await interaction.response.edit_message(embed=embed)
	
	''' Games '''
	@discord.ui.button(label="Games", style=discord.ButtonStyle.primary)
	async def confirmGame(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(title="Here are the available queries!", description="Type the associated slash command to get the query")
		embed.add_field(name="/gt", value="Get 100 entries of the Games table", inline=False)  
		embed.add_field(name="/ghts", value="Find the home team arena gets scored on the most", inline=False)  
		embed.add_field(name="/ghtb", value="Find the arena the home team plays best on", inline=False)
		embed.add_field(name="/glsg", value="Find the longest shootouts in history", inline=False)
		embed.add_field(name="/ghsg", value="Find a list of the highest scoring games (not including shootout goals)", inline=False)
		embed.add_field(name="/gpd", value="List all the games that took place on a given date", inline=False)
		embed.add_field(name="/ghgd", value="List games with the highest goal differential", inline=False)
		embed.add_field(name="/gst", value="Find all games that took place in a given season, played by a specific team, or both", inline=False)
		embed.add_field(name="/ghth", value="List all games played between two teams", inline=False)
		embed.add_field(name="/gha", value="Finds all arenas and the team that calls them home", inline=False)
		await interaction.response.edit_message(embed=embed)
	
	''' Person '''
	@discord.ui.button(label="Person", style=discord.ButtonStyle.primary)
	async def confirmPerson(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(title="Here are the available queries!", description="Type the associated slash command to get the query")
		embed.add_field(name="/pet", value="Get 100 entries of Person table", inline=False)
		embed.add_field(name="/pavh", value="Find the average height of coaches and players in the NHL", inline=False)
		embed.add_field(name="/plbh", value="List all people in the NHL tallest to shortest", inline=False)
		embed.add_field(name="/pdgp", value="Find all people in the database from a given place (city, state, province, or country)", inline=False)
		await interaction.response.edit_message(embed=embed)

	''' Goals '''
	@discord.ui.button(label="Goals", style=discord.ButtonStyle.primary)
	async def confirmGoals(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(title="Here are the available queries!", description="Type the associated slash command to get the query")
		embed.add_field(name="/gtt", value="Get 100 entries of Goals table", inline=False)
		embed.add_field(name="/gsmg", value="Find the shootouts that have had the most goals scored", inline=False)
		embed.add_field(name="/gpsb", value="List all goals by a specific player or in a specific season or both", inline=False)
		embed.add_field(name="/gsg", value="List all goals scored by goalies", inline=False)
		await interaction.response.edit_message(embed=embed)
	

@bot.slash_command(guild_ids=[GUILD_ID], description="Get 100 entries of Games table")
async def gt(ctx):
	await send_table("Games", ctx, 10, 0, 1)

@bot.slash_command(guild_ids=[GUILD_ID], description="Get 100 entries of Head_Coach table")
async def hdt(ctx):
	await send_table("Head_Coach", ctx, 10, 0, 1)

@bot.slash_command(guild_ids=[GUILD_ID], description="Get 100 entries of Person table")
async def pet(ctx):
	await send_table("Person", ctx, 10, 0, 1)

@bot.slash_command(guild_ids=[GUILD_ID], description="Get 100 entries of Team table")
async def tt(ctx):
	await send_table("Team", ctx)

@bot.slash_command(guild_ids=[GUILD_ID], description="Get 100 entries of Team_Stats table")
async def tst(ctx):
	await send_table("Team_Stats", ctx)

@bot.slash_command(guild_ids=[GUILD_ID], description="Get 100 entries of Goals table")
async def gtt(ctx):
	await send_table("Goals", ctx, 10, 0, 1)

@bot.slash_command(guild_ids=[GUILD_ID], description="Get 100 entries of player table")
async def plt(ctx):
	await send_table("player", ctx, 10, 0, 1)

@bot.slash_command(guild_ids=[GUILD_ID], description="run if 'table tmp_view already exists' error occurs")
async def fix(ctx):
	r_sql("Drop view tmp_view")

r_sql("Drop view if exists tmp_view")

bot.load_extension("sql_queries")
bot.run(BOT_TOKEN)
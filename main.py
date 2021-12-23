import discord
from discord.colour import CT
from discord.ext import commands, menus

bot = discord.Bot(intents=discord.Intents().all())

import sqlite3

# from table2ascii import table2ascii, PresetStyle

from tabulate import tabulate
import math

import pandas as pd
import numpy as np
from datetime import datetime

import inspect


conn = sqlite3.connect("hockey_data_final_v2.db")

def r_sql(sql_expr, args=None):
	c = conn.cursor()
	if args:
		c.execute(sql_expr, args)
	else:
		c.execute(sql_expr)
	return c.fetchall()

 
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
	view = Start() # The start menu
	embed = discord.Embed(
		title = "Welcome!",
		description="I'm Sidney Crosbot, feel free to ask me anything about hockey"
	)
	await ctx.respond(embed=embed, view=view)

#Subclass of View used to handle the manin menu
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
  
#Subclass of View storing the different entities
class EntityButtons(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None) 
	
	#When these buttons are clicked, show the available queries according to the labeled table 
	@discord.ui.button(label="Teams", style=discord.ButtonStyle.primary)
	async def confirmTeam(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(
			title="Here are the available queries!",
			description="Type the associated slash command to get the query"
		)
		embed.add_field(name="/tunq", value="Find the teams who've signed the most (unique) players", inline=False)
		embed.add_field(name="/tcgs", value="Find the collective goal stat of a team given a season", inline=False)
		embed.add_field(name="/pss", value="Find the names of all players who have scored an equal number of goals, and assists over the seasons ordered by said number", inline=False)
		await interaction.response.edit_message(embed=embed)
	
	@discord.ui.button(label="Coaches", style=discord.ButtonStyle.primary)
	async def confirmCoach(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(
			title="Here are the available queries!",
			description="Type the associated slash command to get the query"
		)
		embed.add_field(name="/cunq", value="Find the coaches that have coached the most (unique) players while coaching over the years", inline=False)
		embed.add_field(name="/cq", value="This is what the query does", inline=False)
		await interaction.response.edit_message(embed=embed)
		
	@discord.ui.button(label="Players", style=discord.ButtonStyle.primary)
	async def confirmPlayer(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(
			title="Here are the available queries!",
			description="Type the associated slash command to get the query"
		)
		embed.add_field(name="/pxt", value="Find the names of all players who have played in at least x different teams", inline=False)
		embed.add_field(name="/pxot", value="Find the names of all players who have scored at least x goals while in over time", inline=False)
		embed.add_field(name="/pss", value="Find the names of all players who have scored an equal number of goals, and assists over the seasons ordered by said number", inline=False)
		embed.add_field(name="/phsl", value="Find the players who had the highest stat-line for their team in a season", inline=False)
		embed.add_field(name="/psmt", value="Find the names of the players who've signed with the most teams", inline=False)
		# embed.add_field(name="/pss", value="Find the names of all players who have scored an equal number of goals, and assists over the seasons ordered by said number", inline=False)
		# embed.add_field(name="/phsl", value="Find the players who had the highest stat-line for their team in a season", inline=False)
		await interaction.response.edit_message(embed=embed)
		
	@discord.ui.button(label="Games", style=discord.ButtonStyle.primary)
	async def confirmGame(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(
			title="Here are the available queries!",
			description="Type the associated slash command to get the query"
		)
		embed.add_field(name="/gasl", value="Find the arena that tends to start their games the latest", inline=False)
		embed.add_field(name="/ghts", value="Find the home team arena gets scored on the most", inline=False)  
		embed.add_field(name="/ghtb", value="Find the arena the home team plays best on", inline=False)
		await interaction.response.edit_message(embed=embed)
		
	@discord.ui.button(label="Person", style=discord.ButtonStyle.primary)
	async def confirmPerson(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(
		  	title="Here are the available queries!",
			description="Type the associated slash command to get the query"
		)
		embed.add_field(name="/pavh", value="Find the average height of coaches and players in the NHL", inline=False)
		embed.add_field(name="/perq", value="This is what the query does", inline=False)
		await interaction.response.edit_message(embed=embed)

	
async def send_table(table, ctx, entries_per_page=10):
	col_names = tuple(map(lambda x: x[1], r_sql(f"PRAGMA table_info({table});")))
	all_values = r_sql(f"select * from {table}")
	values = r_sql(f"select * from {table} limit 100")
	
	if len(values[0]) >= 7:
		await send_long_table(table, ctx)
		return 
	
	col_name_ascii = " | ".join(col_names) #tabulate([""], col_names, tablefmt="pipe").split('\n')[0]
	table_ascii = tabulate(values ,tablefmt="pipe").split("\n")[1:]

	page_count = math.ceil(len(table_ascii)/entries_per_page)
	
	all_pages = []
	for x in range(page_count):
		desc = "\n".join(table_ascii[x*entries_per_page:(x+1)*entries_per_page])
		if len(table_ascii[0]) > 50:
			desc = desc.replace(" | ", "|")
		all_pages.append(discord.Embed(title="", description=f"```{desc}```"))

	await ctx.respond(embed=discord.Embed(title="", description=f"```{col_name_ascii}```"))
	

	view = discord.ui.View()
	download_button = discord.ui.Button(label="Download as csv", row=1)
	download_button.callback = lambda x: download_csv(x, col_names, all_values, ctx)
	view.add_item(download_button)

	pages = menus.Paginator(pages=all_pages, custom_view=view)
	pages.customize_button("next", button_label=">", button_style=discord.ButtonStyle.blurple)
	pages.customize_button("prev", button_label="<", button_style=discord.ButtonStyle.blurple)
	pages.customize_button("first", button_label="<<", button_style=discord.ButtonStyle.blurple)
	pages.customize_button("last", button_label=">>", button_style=discord.ButtonStyle.blurple)
	await pages.send(ctx, ephemeral=False)

'''
- fix page bug for big tables
- add structure print for big tables

'''

def embed_for_row(rows):
	emb = discord.Embed()
	for row in rows:
		emb.add_field(name=f"{row[1]} ({row[0]})", value="> " + "\n> ".join(map(str, row[2:])), inline=False)
	return emb

async def download_csv(interaction, col_names, values, ctx):
	# df = pd.read_sql_query(f"SELECT * FROM {table}", conn, coerce_float=False)
	df = pd.DataFrame(values, columns=col_names)
	df.astype(int, errors="ignore").to_csv("table.csv", index=False)
	file = discord.File("table.csv", f"{ctx.command.name}_{datetime.now().strftime('%Y-%m-%d_%H.%M')}.csv")
	await interaction.message.reply(file=file)


async def send_long_table(table, ctx):
	col_names = tuple(map(lambda x: x[1], r_sql(f"PRAGMA table_info({table});")))
	all_values = r_sql(f"select * from {table}")
	values = r_sql(f"select * from {table} limit 100")
	
	players_per_page = math.floor(28/len(values[0]))

	col_name_ascii = " | ".join(col_names[1:-1])
	all_pages = []
	for idx in range(0, len(values), players_per_page):
		all_pages.append(embed_for_row(values[idx:idx+players_per_page]))


	struct_emb = discord.Embed(title="Structure")
	struct_emb.add_field(name=f"{col_names[1]} ({col_names[0]})", value="> " + "\n> ".join(map(str, col_names[2:])), inline=False)

	await ctx.respond(embed=struct_emb)

	view = discord.ui.View()
	download_button = discord.ui.Button(label="Download as csv", row=1)
	download_button.callback = lambda x: download_csv(x, col_names, all_values, ctx)
	view.add_item(download_button)
	

	pages = menus.Paginator(pages=all_pages, custom_view=view)
	pages.customize_button("next", button_label=">", button_style=discord.ButtonStyle.blurple)
	pages.customize_button("prev", button_label="<", button_style=discord.ButtonStyle.blurple)
	pages.customize_button("first", button_label="<<", button_style=discord.ButtonStyle.blurple)
	pages.customize_button("last", button_label=">>", button_style=discord.ButtonStyle.blurple)
	await pages.send(ctx, ephemeral=False)




async def custom_sql(template_string, args):
	r_sql(f"CREATE VIEW tmp_view AS {template_string.format(**args)}")
	await send_table("tmp_view", args["ctx"])
	# r_sql("Drop view tmp_view")


@bot.slash_command(guild_ids=[920041129741791294], description="Get 100 entries of Games table")
async def gt(ctx):
	await send_table("Games", ctx)

@bot.slash_command(guild_ids=[920041129741791294], description="Get 100 entries of Head_Coach table")
async def hdt(ctx):
	await send_table("Head_Coach", ctx)

@bot.slash_command(guild_ids=[920041129741791294], description="Get 100 entries of Person table")
async def pet(ctx):
	await send_table("Person", ctx)

@bot.slash_command(guild_ids=[920041129741791294], description="Get 100 entries of Team table")
async def tt(ctx):
	await send_table("Team", ctx)

@bot.slash_command(guild_ids=[920041129741791294], description="Get 100 entries of Team_Stats table")
async def tst(ctx):
	await send_table("Team_Stats", ctx)

@bot.slash_command(guild_ids=[920041129741791294], description="Get 100 entries of player table")
async def plt(ctx):
	await send_table("player", ctx)

@bot.slash_command(guild_ids=[920041129741791294], description="Get 100 entries of player table")
async def long(ctx):
	await send_table("Person", ctx)



''' Extra queries '''
''' structure:
@bot.slash_command(guild_ids=[920041129741791294], description="description")
async def command_name(ctx, argument_name: argument_type = None):
	await custom_sql('sql_command, with {variable_names} (don't forget to add double quotes around name variables (ex: "{name}")', locals())
'''
@bot.slash_command(guild_ids=[920041129741791294], description="Find the names of all players who have scored an equal number of goals, and assists over the seasons")
async def pss(ctx):
        await custom_sql('''SELECT name, goals, assists, season from Person
    NATURAL JOIN player
WHERE goals = assists AND goals > 0
ORDER BY goals DESC;''', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Find the average height of coaches and players in the NHL")
async def pavh(ctx):
        await custom_sql('SELECT ROUND(AVG("height (cm)"),2) AS Average_Height FROM Person;', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Find the arena the home team plays best on")
async def ghtb(ctx):
        await custom_sql('''SELECT arena, COUNT(homeScore) AS Home_Score FROM Games
GROUP BY arena
ORDER BY Home_Score DESC;''', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Find the home team arena gets scored on the most")
async def ghts(ctx):
        await custom_sql('''SELECT arena, COUNT(visitScore) AS Visit_Score FROM Games
GROUP BY arena
ORDER BY Visit_Score DESC;''', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Find the arena that tends to start their games the latest")
async def gasl(ctx):
        await custom_sql('''SELECT arena, FLOOR(AVG(startTime)) AS Start_Time from Games
GROUP BY arena
ORDER BY Start_Time DESC;''', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Find the collective goal stat of a team given a season")
async def tcgs(ctx):
        await custom_sql('''SELECT name, COUNT(goals) AS Goals from Team
    JOIN player p on Team.teamID = p.teamID
GROUP BY Team.name
ORDER BY Goals DESC;''', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Find the names of all players who have played in at least x different teams")
async def pxdt(ctx):
        await custom_sql('''SELECT person.name AS "Name", COUNT(DISTINCT T.name) AS Teams FROM person
    NATURAL JOIN player
    JOIN Team T on player.teamID = T.teamID
GROUP BY personID
HAVING Teams >= ?;''', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Find the names of all players who have scored at least x goals while in over time")
async def pxot(ctx):
        await custom_sql('''SELECT name, COUNT(personID) as goals from Person NATURAL JOIN player JOIN Goals G on player.playerID = G.scorerID
WHERE period like 'OT' AND goals >= ?
GROUP BY personID
ORDER BY goals DESC;
''', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Find the coaches that have coached the most (unique) players while coaching over the years")
async def cunq(ctx):
        await custom_sql('''select P.name, count(DISTINCT X.personID) as numCoached from person P natural join Head_Coach natural join coaches
join (select name, playerID, personID from player natural join person) X on coaches.playerID = X.playerID
group by Head_Coach.personID
order by numCoached DESC LIMIT ?;''', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Find the teams who've signed the most (unique) players")
async def tunq(ctx):
        await custom_sql('''SELECT T.name, COUNT(DISTINCT Players.personID) as numPlayers from Team T
    JOIN (select name, playerID, personID, teamID from player natural join person) Players on T.teamID = Players.teamID
GROUP By T.name
ORDER BY numPlayers DESC;''', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Find the players who’s signed with the most teams")
async def psmt(ctx):
        await custom_sql('''SELECT P.name, COUNT(DISTINCT t.name) AS teamsPlayed from Person P
    NATURAL JOIN player p
    JOIN Team T on p.teamID = T.teamID
GROUP BY personID
ORDER BY teamsPlayed DESC;''', locals())

@bot.slash_command(guild_ids=[920041129741791294], description="description")
async def pcs(ctx, name: str = None):
	await custom_sql('select name, sum(gp) as "Games Played", sum("goals") as "Goals", sum(assists) as "Assists", sum(pts) as "Points", sum(pim) as "PIM" from player natural join person where person.name="{name}" group by personID', locals())

@bot.slash_command(guild_ids=[920041129741791294], description="description")
async def ps(ctx, name: str = None, season: int = None):
	await custom_sql('select name, number, position, season, gp, "goals", assists, pts, pim from player natural join person where name = "{name}" and season = {season}', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="description")
async def pwo(ctx):
	await custom_sql('''select person.name, player.position, sum(gp) as "Total Games Played", sum("goals") as "Total Goals Scored" from person natural join player where position != "G" 
group by personID 
having sum("goals") <  (
select count(personID) as ppGoals from goals join player on goals.scorerID = player.playerID 
natural join person 
where name = "Alex Ovechkin" and goal_type = "PP" 
group by personID) 
order by "Total Goals Scored" DESC
limit 100''', locals())

@bot.slash_command(guild_ids=[920041129741791294], description="description")
async def aaa(ctx):
	await custom_sql('''select * from person natural join player  where pOB like "%Manitoba%"  group by personID order by dOB''', locals())

@bot.slash_command(guild_ids=[920041129741791294], description="description")
async def loc(ctx, loc: str = None):
	await custom_sql('''select * from person natural join player  where pOB like "%{loc}%"  group by personID order by dOB''', locals())

@bot.slash_command(guild_ids=[920041129741791294], description="Find the highest scoring game that didn't go to shootout")
async def sog(ctx):
	await custom_sql('select game_date, arena, count(goal_type) as "Number of Goals" from goals where goal_type != "SO" group by game_date, arena order by "Number of Goals" DESC', locals())


@bot.slash_command(guild_ids=[920041129741791294], description="Best performance by a player in a season where they only played one game")
async def bpp(ctx):
	await custom_sql('select person.name, position, team.name, player.season, gp, "goals", assists, pts from person natural join player natural join plays_for join team on plays_for.teamID = team.teamID order by "gp", pts desc limit 1', locals())

@bot.slash_command(guild_ids=[920041129741791294], description="All clutch players (players that scored a goal with 1 second left to tie the game)")
async def pcg(ctx):
	await custom_sql('''select * from 
(select game_date, arena from goals 
where period = "OT" or period = "Shootout" group by game_date, arena) 
natural join 
(select game_date, arena, name from goals join player on goals.scorerID = player.playerID 
natural join person 
where period = 3 and goal_time = "19:59")''', locals())

@bot.slash_command(guild_ids=[920041129741791294], description="run if 'table tmp_view already exists'")
async def fix(ctx):
	r_sql("Drop view tmp_view")

r_sql("Drop view if exists tmp_view")
bot.run("OTIwMDQ1MTYwMjI0NjU3NDM4.Ybeo0w.XPlqvacAYT2rHPm7OuoKj6Zp1SM")
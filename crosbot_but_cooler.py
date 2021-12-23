import discord
import discord.ext
from discord import guild
from discord import embeds
from discord import emoji
from discord.colour import CT
from discord.ext import menus

bot = discord.Bot()

import sqlite3

# from table2ascii import table2ascii, PresetStyle

from tabulate import tabulate
import math

import pandas as pd
import numpy as np
from datetime import datetime

import inspect


conn = sqlite3.connect("hockey_data.db")

def r_sql(sql_expr, args=None):
	c = conn.cursor()
	if args:
		c.execute(sql_expr, args)
	else:
		c.execute(sql_expr)
	return c.fetchall()

#Subclass of View storing the different entities
class EntityButtons(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None) 
	
	#When these buttons are clicked, show the available queries according to the labeled table 
	@discord.ui.button(label="Teams", style=discord.ButtonStyle.primary)
	async def confirmTeam(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(
			title="Please pick the sample query you wish to see!",
			description="Type the associated slash command to get the query"
		)
		embed.add_field(name="/tc", value="This is what the query does", inline=False)
		embed.add_field(name="/tq", value="This is what the query does", inline=False)
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
		
	@discord.ui.button(label="Person", style=discord.ButtonStyle.primary)
	async def confirmPerson(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(
		  title="Please pick the sample query you wish to see!",
			description="Type the associated slash command to get the query"
		)
		embed.add_field(name="/perc", value="This is what the query does", inline=False)
		embed.add_field(name="/perq", value="This is what the query does", inline=False)
		await interaction.response.edit_message(embed=embed)


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
			 
#Used to initiate the main menu
@bot.slash_command(guild_ids=[920041129741791294])
async def start(ctx):   
	view = Start() # The start menu
	embed = discord.Embed(
		title = "Welcome!",
		description="I'm Sidney Crosbot, feel free to ask me anything about hockey"
	)
	await ctx.respond(embed=embed, view=view)
	

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

bot.run("OTIwMDQ1MTYwMjI0NjU3NDM4.Ybeo0w.XPlqvacAYT2rHPm7OuoKj6Zp1SM")
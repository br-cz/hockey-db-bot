import sqlite3
import math
import numpy as np
import pandas as pd
from tabulate import tabulate
from datetime import datetime
import discord
from discord.ext import commands, menus

conn = sqlite3.connect("hockey_decade.db")

def r_sql(sql_expr, args=None):
	c = conn.cursor()
	if args:
		c.execute(sql_expr, args)
	else:
		c.execute(sql_expr)
	return c.fetchall()


async def send_table(table, ctx, entries_per_page=10, force_send_short_table=True, force_send_long_table=False):
	col_names = tuple(map(lambda x: x[1], r_sql(f"PRAGMA table_info({table});")))
	all_values = r_sql(f"select * from {table}")
	values = r_sql(f"select * from {table} limit 100")
	
	try:
		if (len(values[0]) >= 6 or force_send_long_table) and not force_send_short_table:
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
	except Exception:
		await ctx.respond(embed=discord.Embed(title="Oops!", description = "Sorry, this query didn't return any results. Please try a different query."))
		return
	

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

def embed_for_row(rows):
	emb = discord.Embed()
	for row in rows:
		emb.add_field(name=f"{row[1]} ({row[0]})", value="> " + "\n> ".join(map(str, row[2:])), inline=False)
	return emb

async def download_csv(interaction, col_names, values, ctx, convert_to_int=False):
	# df = pd.read_sql_query(f"SELECT * FROM {table}", conn, coerce_float=False)
	df = pd.DataFrame(values, columns=col_names)
	if convert_to_int:
		df = df.astype(int, errors="ignore")
	df.to_csv("table.csv", index=False)
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

async def custom_sql(template_string, args, force_send_short_table=True, force_send_long_table=False):
	r_sql(f"CREATE VIEW tmp_view AS {template_string.format(**args)}")
	await send_table("tmp_view", args["ctx"], force_send_short_table=force_send_short_table, force_send_long_table=force_send_long_table)
	r_sql("Drop view if exists tmp_view")

from bot_utils import *
from config import *
from discord.colour import CT
from discord.commands import slash_command, Option

''' Extra queries '''
class ExtraSQLQueries(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@slash_command(guild_ids=[GUILD_ID], description="Find the names of all players who have scored an equal number of goals, and assists over the seasons")
	async def pss(self, ctx):
			await custom_sql('''SELECT name, goals, assists, season from Person
		NATURAL JOIN player
	WHERE goals = assists AND goals > 0
	ORDER BY goals DESC;''', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the average height of coaches and players in the NHL")
	async def pavh(self, ctx):
			await custom_sql('SELECT ROUND(AVG("height (cm)"),2) AS "Average_Height (cm)" FROM Person;', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the arena the home team plays best on")
	async def ghtb(self, ctx):
			await custom_sql('''SELECT arena, COUNT(homeScore) AS Home_Score FROM Games
	GROUP BY arena
	ORDER BY Home_Score DESC;''', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the home team arena gets scored on the most")
	async def ghts(self, ctx):
			await custom_sql('''SELECT arena, COUNT(visitScore) AS Visit_Score FROM Games
	GROUP BY arena
	ORDER BY Visit_Score DESC;''', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the names of all players who have played in at least x different teams")
	async def pxdt(self, ctx, num_teams: Option(int, "Number of different teams", default=2)):
			await custom_sql('''SELECT person.name AS "Name", COUNT(DISTINCT T.name) AS Teams FROM person
		NATURAL JOIN player
		JOIN Team T on player.teamID = T.teamID
	GROUP BY personID
	HAVING Teams >= {num_teams};''', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the coaches that have coached the most (unique) players while coaching over the years")
	async def cunq(self, ctx):
			await custom_sql('''select P.name, count(DISTINCT X.personID) as numCoached from person P natural join Head_Coach natural join coaches
	join (select name, playerID, personID from player natural join person) X on coaches.playerID = X.playerID
	group by Head_Coach.personID
	order by numCoached DESC LIMIT 100;''', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the teams who've signed the most players in total")
	async def tunq(self, ctx):
			await custom_sql('''SELECT T.name, COUNT(DISTINCT Players.personID) as numPlayers from Team T
		JOIN (select name, playerID, personID, teamID from player natural join person) Players on T.teamID = Players.teamID
	GROUP By T.name
	ORDER BY numPlayers DESC;''', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the players who've played for the most teams")
	async def psmt(self, ctx):
			await custom_sql('''SELECT P.name, COUNT(DISTINCT t.name) AS teamsPlayed from Person P
		NATURAL JOIN player p
		JOIN Team T on p.teamID = T.teamID
	GROUP BY personID
	ORDER BY teamsPlayed DESC;''', locals())


	 
	@slash_command(guild_ids=[GUILD_ID], description="Find the players who had the highest stat-line for their team in a season")
	async def phsl(self, ctx, season: Option(int, "Specific season you want to query", default=20202021, required=False	)):
		await custom_sql('''SELECT T.name as "Team", Person.name AS Player, goals AS Goals, assists AS Assists, max(pts) AS Points, T.season from Person
		 NATURAL JOIN player
		 JOIN Team T on player.teamID = T.teamID
	WHERE T.season = {season}
	GROUP BY T.name order by T.name;''', locals(), 0 , 1)

	@slash_command(guild_ids=[GUILD_ID], description="Find the oldest active players in the NHL")
	async def pold(self, ctx):
		await custom_sql("select name, cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', dOB) as int) as \"Age\"from person natural join player where season = 20202021 order by age DESC", locals())	

	@slash_command(guild_ids=[GUILD_ID], description="Find all people in the database from a specified place (city, state, province, or country)")
	async def pdgp(self, ctx, location: Option(str, "The location (city, state, province, or country) you want to query", default=None)):
		await custom_sql('select * from person where pOB like "%{location}%"  group by personID order by dOB limit 100', locals(), 0, 1)

	@slash_command(guild_ids=[GUILD_ID], description="Find the best goal scorer from a specified place")
	async def pbgs(self, ctx, location: Option(str, "The location (city, state, province, or country) you want to query", default=None)):
		await custom_sql('select dOB, name, pOB, sum(gp) as Games_Played, sum(Player.goals) as G, sum(assists) as A, sum(pts) as Points, sum(PIM) as PM from person natural join player  where pOB like "%{location}%"  group by personID order by G DESC', locals(), 0, 1)

	@slash_command(guild_ids=[GUILD_ID], description="Find all the players that have scored with 1 second left on the clock to bring the game to overtime")
	async def posl(self, ctx):
		await custom_sql('''select * from
	(select game_date, arena from goals
	where period = "OT" or period = "Shootout" group by game_date, arena)
	natural join
	(select game_date, arena, name from goals join player on goals.scorerID = player.playerID
	natural join person
	where period = 3 and goal_time = "19:59")''', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find all the players that have scored less across their career than Alex Ovechkin on the powerplay")
	async def plao(self, ctx):
		await custom_sql('''select person.name, player.position, sum(gp) as "Total Games Played", sum("goals") as "Total Goals" from person natural join player where position != "G"
	group by personID
	having sum("goals") <  (
	select count(personID) as ppGoals from goals join player on goals.scorerID = player.playerID
	natural join person
	where name = "Alex Ovechkin" and goal_type = "PP"
	group by personID)
	order by "Total Goals" DESC
	limit 100''', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find all the Hockey players and the # of coaching changes they've had while playing for 1 team")
	async def pncc(self, ctx):
		await custom_sql('''select person.name, count(distinct Head_Coach.personID) as "Number of Coaches" from person natural join player natural join coaches
	join Head_Coach on coaches.coachID = Head_Coach.coachID where person.personID in
	(select personID from person natural join player join team ON player.teamID = team.teamID
		group by personID
		having count(distinct team.name) = 1
		order by person.name)
	group by person.personID order by "Number of Coaches" DESC
	limit 100''', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the best teams at scoring on the penalty kill in a single season")
	async def tspk(self, ctx):
		await custom_sql('''select team.name, team.season, count(name) as "Goals_Scored" from goals join player P on scorerID = P.playerID
	join team on P.teamID = team.teamID where goal_type like "SH%"
	group by team.name, team.season
	order by Goals_Scored desc
	limit 100''', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the best performing players in a season where they only played one game (with that team)")
	async def psg(self, ctx):
		await custom_sql('''select position, person.name as "Name", team.name as "Team", player.season, gp, "goals", assists, pts from person natural join player
	join team on player.teamID = team.teamID
	order by "gp", pts desc
	limit 100''', locals(), 0, 1)


	@slash_command(guild_ids=[GUILD_ID], description="Find the first goal scored by a specific player with a specific team")
	async def pfgt(self, ctx, name: Option(str, "The player whose first goal you want to find", default=None, required = True), team: Option(str, "The team you want to query", default=None, required=True)):
		await custom_sql('''select team.name AS "Team", person.name as "Name", team.season, game_date, arena, goal_time, period, goal_type from person natural join player
	join team on player.teamID = team.teamID join goals on player.playerID = goals.scorerID
	where person.name = "{name}" AND team.name = "{team}"
	order by game_date limit 1''', locals(), 0, 1)


	@slash_command(guild_ids=[GUILD_ID], description="Find a list of the highest scoring games (not including shootout goals)")
	async def ghsg(self, ctx):
		await custom_sql('select game_date, arena, count(goal_type) as "Number of Goals" from goals where goal_type != "SO" group by game_date, arena order by "Number of Goals" DESC', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the shootouts that have had the most goals scored")
	async def gsmg(self, ctx):
		await custom_sql('select game_date, arena, count(goal_time) as "Total Goals Scored" from goals where goal_type = "SO" group by game_date, arena order by "Total Goals Scored" DESC', locals())


	@slash_command(guild_ids=[GUILD_ID], description="Find the longest shootouts in history")
	async def glsg(self, ctx):
		await custom_sql('''select game_date, arena, max(cast("goal_time" as int))/2 + max(cast("goal_time" as int))%2 as "Shootout Round"
	from goals where goal_type = "SO"
	group by game_date, arena
	order by "Shootout Round" desc, game_date
	limit 100''', locals())

	@slash_command(guild_ids=[GUILD_ID], description="Find the players with the most goals in one game")
	async def pmgo(self, ctx):
		await custom_sql('''select game_date, arena, name, count(scorerID) AS "Number of Goals Scored"
	from goals join player on scorerID = playerID natural join person
	group by game_date, arena, scorerID
	order by "Number of Goals Scored" DESC''', locals(),0,1)

	@slash_command(guild_ids=[GUILD_ID], description="Find the standings for a specified season")
	async def tss(self, ctx, season: Option(int, "The season whose results you want (default: 20202021)", default=20202021, required=False)):
		await custom_sql('''select * from team_stats where season = {season} 
	order by pts desc''', locals(), 1)

	@slash_command(guild_ids=[GUILD_ID], description="Find franchise stats for a given team")
	async def tsf(self, ctx, team_name: Option(str, "The team you want to query (Default: Winnipeg Jets)", default="Winnipeg Jets", required=False)):
		await custom_sql('''select name, sum(gp) as "Games", sum(wins) as "Wins", sum(losses) as "Losses", sum(OTL) as OTL, sum(SOL) as SOL, sum(pts) as "Points" from team_stats 
	where name = "{team_name}"
	group by name''', locals(), 1)

	@slash_command(guild_ids=[GUILD_ID], description="Find the stats for a specific team, season, or both")
	async def tsts(self, ctx, season: Option(int, "The season whose stats you want to find (Default: 20202021)", default=20202021, required=False), team_name: Option(str, "The team whose stats you want to find (Default: Winnipeg Jets)", required=False, default="Winnipeg Jets")):
		await custom_sql('''select * from team_stats
	where name = "{team_name}" AND season = {season}''', locals())

	@slash_command(guild_ids=[GUILD_ID], description="Find the most dominant teams of all time (most wins, least losses, OTL, and SOL)")
	async def tsmd(self, ctx):
		await custom_sql('''select * from Team_Stats
	order by (wins - losses - OTL - SOL) DESC	''', locals(), 1)

	@slash_command(guild_ids=[GUILD_ID], description="Find the teams with the largest number of unique players in one season")
	async def tmup(self, ctx):
		await custom_sql('''select team.name, team.season, count(playerID) as "Number of Players" 
	from team natural join team_stats join player on team.teamID = player.teamID 
	group by team.teamID 
	order by "Number of Players" DESC''', locals())

	@slash_command(guild_ids=[GUILD_ID], description="Find all teams that a specific player has played for")
	async def tpp(self, ctx, player_name: Option(str, "The player you want to query (Default: Blake Wheeler)", default="Blake Wheeler", required=False)):
		await custom_sql('''select team.name, team.season from team natural join team_stats join player on team.teamID = player.teamID join person on player.personID = person.personID
	where person.name = "{player_name}"''', locals())

	@slash_command(guild_ids=[GUILD_ID], description="Find the head coaches that have worked for the most teams")
	async def hcmt(self, ctx):
		await custom_sql('''select person.name, count(distinct team.name) as "Number of Teams" from person natural join Head_Coach join team on Head_coach.teamID = team.teamID
	group by personID
	order by "Number of Teams" DESC''', locals())

	@slash_command(guild_ids=[GUILD_ID], description="List all head coaches with career stats ordered by a specified statistic")
	async def hcos(self, ctx, stat: Option(str, "The stat you want to order by", choices=["Games", "Wins", "Losses", "OTL"])):
		await custom_sql('''select sum("GP") as "Total Games", name,  sum("Wins") as "Total Wins", sum(losses) as "Total Losses", sum(OTL) as "Total OTL" from person natural join head_coach group by personID
	order by "Total {stat}" DESC''', locals(), 0, 1)

	@slash_command(guild_ids=[GUILD_ID], description="List all head coaches with career stats ordered by a specified statistic")
	async def pcos(self, ctx, stat: Option(str, "The stat you want to order by", choices=["Games", "Goals", "Assists", "Points", "Penalty Minutes"])):
		await custom_sql('select sum(gp) as "Total Games", name, sum("Goals") as "Total Goals", sum(assists) as "Total Assists", sum("pts") as "Total Points", sum("PIM" ) as "Total Penalty Minutes" from person natural join player group by personID order by "Total {stat}" DESC', locals(), 0, 1)

	@slash_command(guild_ids=[GUILD_ID], description="List all the games that took place on a specified date")
	async def gpd(self, ctx, date: Option(str, "The date which you want to fetch games for", default=None)):
		await custom_sql('''select game_date, arena, Home.name as "Home Team", homeScore as "Home Score", Visit.name as "Visiting Team", visitScore as "Visiting Score" 
	from games join team Home on homeTeam = Home.teamID join team Visit on visitTeam = Visit.teamID
	where game_date = "{date}"''', locals(), 0, 1)

	@slash_command(guild_ids=[GUILD_ID], description="List games with the highest goal differential")
	async def ghgd(self, ctx):
		await custom_sql('''select game_date, arena, Home.name as "Home Team", homeScore as "Home Score", Visit.name as "Visiting Team", visitScore as "Visiting Score" 
	from games join team Home on homeTeam = Home.teamID join team Visit on visitTeam = Visit.teamID
	order by abs("Home Score" - "Visiting Score") DESC''', locals(), 0, 1)

	@slash_command(guild_ids=[GUILD_ID], description="Find all games that took place in a specified season or played by a specific team, or both")
	async def gst(self, ctx, season: Option(int, "The season you want to query (Default: 20202021)", default=20202021, required=False), team_name: Option(str, "The team you want to query (Default: Winnipeg Jets)", default="Winnipeg Jets", required=False)):
		await custom_sql('''select game_date, arena, Home.name as "Home Team", homeScore as "Home Score", Visit.name as "Visiting Team", visitScore as "Visiting Score" 
	from games join team Home on homeTeam = Home.teamID join team Visit on visitTeam = Visit.teamID
	where ("Home Team" = "{team_name}" OR "Visiting Team" = "{team_name}") AND home.season = {season}''', locals(), 0, 1)

	@slash_command(guild_ids=[GUILD_ID], description="List all people in the NHL tallest to shortest")
	async def plbh(self, ctx):
		await custom_sql('select * from person order by "height (cm)" desc', locals(), 0, 1)

	@slash_command(guild_ids=[GUILD_ID], description="List all goals by a specific player or in a specific season or both")
	async def gpsb(self, ctx, season: Option(int, "The season you want to query (Default: 20202021)", default=20202021, required=True), player: Option(str, "The player whose goals you want to find (Default: Nikolaj Ehlers)", default="Nikolaj Ehlers", required=False)):
		await custom_sql('''select game_date as "Date", arena as "Arena", goal_time, period, goal_type from goals join player on scorerID = playerID natural join Person
	where name = "{player}" AND season = {season}''', locals(), 0)

	@slash_command(guild_ids=[GUILD_ID], description="List players with the number of games in which they scored >= 3 goals")
	async def phtm(self, ctx):
		await custom_sql('''select name, count(name) as "Total Games Scoring 3 or more goals" from 
	(
	select game_date, arena, name, count(scorerID) AS "Number of Goals Scored" 
	from goals join player on scorerID = playerID natural join person 
	group by game_date, arena, scorerID having "Number of Goals Scored" > 2 
	order by "Number of Goals Scored" DESC
	)
	group by name
	order by "Total Games Scoring 3 or more goals" DESC
	limit 100''', locals())

	@slash_command(guild_ids=[GUILD_ID], description="List all games played between two teams")
	async def ghth(self, ctx, first_team: Option(str, "The first team whose head-to-head games you want", default=None), second_team: Option(str, "The second team whose head-to-head games you want", default=None)):
		await custom_sql('''select game_date, arena, Home.name as "Home Team", homeScore as "Home Score", Visit.name as "Visiting Team", visitScore as "Visiting Score" 
	from games join team Home on homeTeam = Home.teamID join team Visit on visitTeam = Visit.teamID
	where ("Home Team" = "{first_team}" OR "Visiting Team" = "{first_team}") AND ("Home Team" = "{second_team}" OR "Visiting Team" = "{second_team}")''', locals(), 0, 1)

	@slash_command(guild_ids=[GUILD_ID], description="Finds all arenas and the team that calls them home")
	async def gha(self, ctx):
		await custom_sql('''select game_date, arena, Home.name as "Home Team"
	from games join team Home on homeTeam = Home.teamID join team Visit on visitTeam = Visit.teamID
	group by arena, "Home Team"
	order by "Home Team"''', locals())

	@slash_command(guild_ids=[GUILD_ID], description="List all goals scored by goalies")
	async def gsg(self, ctx):
		await custom_sql('''select game_date, name, arena, goal_time, period, goal_type from goals join player on scorerID = playerID natural join person
			where position = "G"
			order by game_date desc''', locals(),0,1)

def setup(bot):
	print("Extra sql queries slash commands loaded")
	bot.add_cog(ExtraSQLQueries(bot))
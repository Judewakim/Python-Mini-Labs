from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

printer = PrettyPrinter()

#get links to all information
def get_links() :
    data = get(BASE_URL + ALL_JSON).json()
    links = data['links']
    return links

#gets live scoreboard
def get_scoreboard(): 
    scoreboard = get_links()['currentScoreboard']
    games = get(BASE_URL + scoreboard).json()['games']

    for game in games:  
        home_team = game['hTeam']
        away_team = game['vTeam']
        clock = game['clock']
        period = game['period']
        year = game['seasonYear']
        
        print("-----------------------")
        print(f"{home_team['triCode']} vs {away_team['triCode']}")
        print(f"{home_team['score']} - {away_team['score']}")
        print(f"{clock} - {period['current']}Q")

#gets avg ppg ranked
def get_team_stats():
    stats= get_links()['leagueTeamStatsLeaders']
    teams = get(BASE_URL + stats).json()['league']['standard']['regularSeason']['teams']

    #filters all teams != to 'name' removing all teams that dont have 'name' like allstar teams
    teams = list(filter(lambda x: x['name'] != "Team", teams))
    # #sorting 
    teams.sort(key=lambda x: x['ppg']['rank'])

    for team in teams:
        name = team['name']
        nickname = team['nickname']
        ppg = team['ppg']['avg']
        print(f"{name} {nickname} - {ppg}ppg")


#get playoff bracket -WORKING
def get_playoff_bracket():
    info = get_links()['playoffsBracket']
    playoff_teams = get(BASE_URL + info).json()

   
get_scoreboard()

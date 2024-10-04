"""Libraries"""
from selenium import webdriver #Selenium -> webdriver: Used to connect web driver to program
from selenium.webdriver.chrome.service import Service #Selenium -> Service
from selenium.webdriver.chrome.options import Options #Selenium -> Options: Allows for custom options to be called
from selenium.webdriver.common.by import By #Selenium -> By: Allows for calls by specific variables from html code
from webdriver_manager.chrome import ChromeDriverManager #Webdriver_manager -> ChromeDriverManager: Allows for chrome driver to be ran
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import json
from class_file import Player
from utils import openJsonFile

"""Functionality functions"""
def loadDriver(url): #Loads driver
    """Selenium"""
    options = Options() #intialize option variable to class Options
    options.add_argument('--headless') #Take away window from being open on program run
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options) #Initializes driver var to chrome driver
    driver.get(url) #URL for what html page I want
    driver.implicitly_wait(10) #Makes driver wait 10 ms before doing anything: Allows for everything to load before accessing HTML elements
    print(f"Driver loaded: {driver} with link: {url}")
    return driver

def loadGame(url): #Loads specific game to get JSON file from game
    payload = ""
    headers = {"User-Agent": "insomnia/10.0.0"}
    
    response = requests.get(url,headers=headers)
    game_data = response.json()
    
    game_file = 'game.json'

    with open(game_file,'w') as json_file:
        json.dump(game_data,json_file, indent=4)

    print(f"Data has been saved to {game_file}")

    return game_file

def loadPlayerProfile(url):
    querystring = {"playlist":"competitive","season_id":"292f58db-4c17-89a7-b1c0-ba988f0e9d98"}
    payload = ""
    headers = {"User-Agent": "insomnia/10.0.0"}

    response = requests.get(url, data=payload, headers=headers, params=querystring)
    player_data = response.json()

    player_file = 'player.json'

    with open(player_file,'w') as json_file:
        json.dump(player_data,json_file,indent=4)
    
    print(f"Player data has been saved to {player_file}")
    
    return player_file

def loadCharacterStats(url):
    querystring = {"playlist":"competitive","season_id":"292f58db-4c17-89a7-b1c0-ba988f0e9d98"}
    payload = ""
    headers = {"User-Agent": "insomnia/10.0.0"}

    response = requests.get(url, data=payload, headers=headers, params=querystring)
    character_data = response.json()

    character_file = 'characters.json'

    with open(character_file,'w') as json_file:
        json.dump(character_data,json_file,indent=4)
    
    print(f"Character data has been saved to {character_file}")
    
    return character_file

def loadWeaponStats(url):
    querystring = {"playlist":"competitive","season_id":"292f58db-4c17-89a7-b1c0-ba988f0e9d98"}
    payload = ""
    headers = {"User-Agent": "insomnia/10.0.0"}

    response = requests.get(url, data=payload, headers=headers, params=querystring)
    character_data = response.json()

    weapons_file = 'weapons.json'

    with open(weapons_file,'w') as json_file:
        json.dump(character_data,json_file,indent=4)
    
    print(f"Weapon data has been saved to {weapons_file}")
    
    return weapons_file

def create_players(game): #Creates Player class and adds the player name and team to the class
    teams = assignTeam(game)

    players = []
    for team,names in teams.items():
        for name in names:
            player = Player(name,team)
            players.append(player)
    return players        

def getGameLinksForStratsGG(link): #Gets LAST FIVE GAMES PLAYED links, uses strats.gg overview page
    strats = loadDriver(link) #Load driver
    game_list = [] 

    game_links = strats.find_elements(By.CSS_SELECTOR, "a.match") #a.match: match is the CSS selector, a is the anchor tag
    all_links = [link.get_attribute('href') for link in game_links] #Just get the links

    for href in all_links:
        game_list.append(href) #Add links to list
    
    strats.quit()
    return game_list[:4] #Return last give games played



"""Overview stats functions"""
def getOverallStats(link):  # Gets overall stats and adds them to one tuple
    driver = loadDriver(link)
    
    try:
        # Wait up to 9 seconds for each element to load; move on if not found
        kd = getKD(driver) or "N/A"  # Return "N/A" if KD is not found
        winp = getWinPercentage(driver) or "N/A"
        top_agent = getTopAgent(driver) or "N/A"
        headshot_percentage = getHeadShotPercentage(driver) or "N/A"
        
    except TimeoutException:
        print("Some elements took too long to load, moving on with available data.")
        # Handle the case where some of the elements take too long to load or aren't found.
        kd, winp, top_agent, headshot_percentage = "N/A", "N/A", "N/A", "N/A"
    
    finally:
        driver.quit()
    
    return kd, winp, top_agent, headshot_percentage

def getKD(player): #Gets kd for a player, uses API call to get json player file for player
    data = openJsonFile(player)
    
    stats = data['stats']
    kd = stats['kd_ratio']
    
    #print(kd)
    return kd

def getWinPercentage(player): #Gets win percentage for a player, uses API call to get json player file for player
    data = openJsonFile(player)
    
    stats = data['stats']
    wins = stats['matches_won']
    played = stats['matches_played']
    winp = round((wins/played) * 100)

    #print(winp)
    return winp

def getTopAgent(player): #Gets top agent for a player, uses API call to get json character file for player
    data = openJsonFile(player)
    
    agent_list = data['characters']
    top_agent = agent_list[0]
    top_agent_info = top_agent['character']
    top_agent_name = top_agent_info['name']
    
    print(top_agent_name)
    return top_agent_name

def getHeadShotPercentage(player): #Gets headshot percentage for a player, uses API call to get json player file for player
    data = openJsonFile(player)
    
    stats = data['stats']
    hs_perc = stats['headshots_percent']
    
    print(hs_perc)
    return hs_perc

def getKnifeKills(player): #Gets knife kills for a player, uses API call to get json weapon file for player
    data = openJsonFile(player)
    
    weapons_list = data['weapons']
    
    for weapon in weapons_list: #Iterates through each weapon
        name = weapon['metadata']['name']
        kills = weapon['stats']['kills']
        if "Melee" in name: #Limits to only knife kills
            knife_kills = kills
    
    #print(knife_kills)
    return knife_kills

def get149DamageDone(url): #Calculate the amount of times 149 damage is done
    driver = loadDriver(url) #load driver
 
    word = "Phantom" #Looks for phantom
    get_table = driver.find_elements(By.CSS_SELECTOR,'tr') #Gets table
    for row in get_table: #Get individual rows
        row = row.text
        
        if word in row: #Only store row with phantom in it
            phantom_stats = row.split('\n') #Get rid of new line characters
            
    hits_with_a_kill = float(phantom_stats[3]) #Get kill conversion, change it float
    head_shot_percentage = float(phantom_stats[6].replace('%', '')) #Get rid of % sign in hs%, change it to float
    head_shot_percentage = head_shot_percentage/100 #Change hs% into decimal value
    
    #Will need to simplify and correct these naming conventions later
    total_hits = phantom_stats[7:] #Limit to just hits stats
    total_hits = [item.split('(')[1].split(')')[0] for item in total_hits] #Splits at both parentheses and grabs just the number of hits
    float_hits = [float(item) for item in total_hits] #Floatifiies number of hits
    sum_of_hits = sum(float_hits) #Sums all hit values
    
    #Calculating 149 Damage Done
    hits_without_a_kill = 1.0 - hits_with_a_kill #Get hits without a kill
    
    head_shots_without_a_kill = head_shot_percentage * hits_without_a_kill #Compute head shots withotu a kill
    one_four_nine_damage_done = int(sum_of_hits * head_shots_without_a_kill) #Get amount of times 149 damage is done

    
    driver.quit() #Quit driver
    return one_four_nine_damage_done

"""Single game stats"""
def getStatsForOneGame(link): #Gets stats for one SINGLE GAME, uses strats.gg game page
    game = loadDriver(link) #Load driver with strats.gg link
    stat_list = [] 
    
    stats = game.find_elements(By.CLASS_NAME, 'compare-table__row') #Find stats
    
    for stat in stats:
        stat = stat.text #Get text
        stat = '\n'.join(stat.split('\n')[:2]) #Split at \n, only take first two positions, add them back together
        stat = stat.replace("\n"," ") #Replace new line character with space
        stat_list.append(stat) #Add stat to list
   
    game.quit() #close driver
    return stat_list #Return game stats

def findEconomyAverage(driver):
    all_players_economy = []

    while True:
        try:
            economy_column = driver.find_elements(By.CLASS_NAME, 'col-economy')
            for econ in economy_column:
                if econ.text == "Econ":
                    continue
                all_players_economy.append(econ.text)
            break  # Break if everything is fine
        except StaleElementReferenceException:
            continue  # Retry fetching elements if stale

    player_team_econ = all_players_economy[0:5]
    enemy_team_econ = all_players_economy[5:]

    int_player_econ = [int(item) for item in player_team_econ]
    avg_player_econ = sum(int_player_econ) / len(player_team_econ)
    int_enemy_econ = [int(item) for item in enemy_team_econ]
    avg_enemy_econ = sum(int_enemy_econ) / len(enemy_team_econ)
    
    return avg_player_econ, avg_enemy_econ

def findWinOrLoss(driver):
    #driver = loadDriver(url)
    win_or_loss = []
    find_win_or_loss = driver.find_elements(By.CSS_SELECTOR,'span.title.type-subtitle--bold')
    for game in find_win_or_loss:
        win_or_loss.append(game.text)
    
    last_5_games = win_or_loss[:5]
    
    
    return last_5_games

def getGameLinksForBlitzGG(driver):
    #driver = loadDriver(url)
    game_list = []
    game_links = driver.find_elements(By.CSS_SELECTOR,'a.match-link')
    all_links = [link.get_attribute('href') for link in game_links]

    for href in all_links:
        game_list.append(href)
    last_five_game_links = game_list[:5]
    
    return last_five_game_links

def calculateAntiThrifties(url):
    driver = loadDriver(url)
    game_links = getGameLinksForBlitzGG(driver)
    game_outcomes = findWinOrLoss(driver)
    
    results = {}
    anti_thrifted = 0
    thrifties = 0
    for index, link in enumerate(game_links):
        game = loadDriver(link)
        econ_averages = findEconomyAverage(game)

        #Add results to dictionary with index as key
        results[f"Game {index + 1}"] = {
            "Outcome": game_outcomes[index],
            "Average Player Econ": econ_averages[0],
            "Average Enemy Econ": econ_averages[1]
        }
    
    for game,data in results.items():
        if data["Outcome"] == 'Defeat' and data["Average Player Econ"] > data["Average Enemy Econ"]:
            anti_thrifted += 1
        elif data["Outcome"] == 'Victory' and data["Average Player Econ"] < data["Average Enemy Econ"]:
            thrifties += 1
        else:
            print("No links between econ and outcome of game")
    print(anti_thrifted)
    print(thrifties)

    driver.quit()



"""Following functions work all together to create round by roud Win% Algo"""
def getPlayersInGame(game): #Gets the names of players in a game, intakes a JSON game file
    game = openJsonFile(game)
    player_list = []
    
    players = game['match']['players']
    
    for player in players:
        platform_info = player['platform_info']
        name = platform_info['platform_user_nick']
        player_list.append(name)
    
    return player_list

def getAvgTeamWinPercentage(players): #Takes in a list of players from a game, gets average winp for each team
    #Lists for teams
    all_players = [] 
    team_1 = [] 
    team_2 = [] 

    for player in players: #goes through players, creates link, loads that link to get JSON file, uses JSON file to get win percentage, adds winp to list
        link = createAPIPlayerLink(player)
        player_data = loadPlayerProfile(link)
        winp = getWinPercentage(player_data)
        winp = float(winp)
        all_players.append(winp)

    #Specify which team is which
    team_1 = all_players[:5]
    team_2 = all_players[5:]
    
    #Creates the average winp for each team
    team_1_winp = round(sum(team_1)/len(team_1))
    team_2_winp = round(sum(team_2)/len(team_2))
    
    #print(team_1_winp)
    #print(team_2_winp)

    return team_1_winp,team_2_winp

def findRoundOutcome(game): #Finds what team won each round for a game, returns dict
    with open(game,'r') as json_file:
        data = json.load(json_file)

    round_outcome = {}
    rounds = data['match']['rounds'] #limit to rounds sub-cat for match

    for round_data in rounds: #gets round num and the team that won for each round, adds to dictionary
        round_num = round_data['round_num']
        winning_team = round_data['winning_team']
        round_outcome[round_num] = winning_team

    #print(round_outcome)
    return round_outcome

def assignTeam(game): 
    with open(game, 'r') as json_file:  # Load game file
        data = json.load(json_file)

    teams_dict = {"Red": [], "Blue": []}  # Initialize dictionary with two keys: Red and Blue

    players = data['match']['players']  # Limit to match -> players

    for player in players:  # For each player, get name and team_id
        platform_info = player['platform_info']
        name = platform_info['platform_user_nick']

        team_name = player['metadata']['team_id']  # match -> players -> metadata: team
        
        if "Red" in team_name:
            teams_dict["Red"].append(name)
        elif "Blue" in team_name:
            teams_dict["Blue"].append(name)

    return teams_dict  # Return the dictionary with the teams
                        
def getKillsPerRound(game): #Gets kills for each player for each round, using strats gg API and json file, returns dict
    with open(game,'r') as json_file:
        data = json.load(json_file) #Load json_file for game
    round_dict = {} #Create dictionary
    players = data['match']['players'] #Limit to match -> Players
    
    for player in players: #For each player
        platform_info = player['platform_info'] #limit to match -> Players -> platform_info
        name = platform_info['platform_user_nick'] #gets name of player match -> Players -> platform_info: name
        
        if name not in round_dict:
            round_dict[name] = {} #if the name is not in the dicitonary, put it ther

        rounds = player['round_results'] #Limit to round results, match -> players -> round_results

        for round_data in rounds: #iterate through each round to get kills and round number
            round_num = round_data['round_num'] #match -> players -> round_results: round_num
            kills = round_data['kills'] #match -> players -> round_results: kills
            
            round_dict[name][round_num] = kills #Store into dictionary with name as the key
    
    #print(round_dict)
    return round_dict

"""Python Functionality Functions""" #USED WITH GETAVGTEAMWINPERC
def createPlayerLink(x): #Gives a strats.gg outline based on the player name that was inserted
    num_of_spaces = x.count(" ")
    if num_of_spaces == 1:
        split = x.split(" ")
        p_name = split[0]
        p_id = split[1]
        link = f"https://www.strats.gg/valorant/stats/{p_name}%23{p_id}/overview"
        print(f"Link created {link}")
        return link
    else:
        split = x.split(" ")
        p_name1 = split[0]
        p_name2 = split[1]
        p_id = split[2]
        link = f"https://www.strats.gg/valorant/stats/{p_name1}%20{p_name2}%23{p_id}/overview"
        print(f"Link created {link}")
        return link

def createAPIPlayerLink(player): #Takes in player name,Creates outline for API link, returns link created
    num_of_spaces = player.count(" ")
    if num_of_spaces == 1:
        split = player.split("#")
        name = split[0]
        id = split[1]
        split_name = name.split(" ")
        name1 = split_name[0]
        name2 = split_name[1]
        url = f"https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/{name1}%20{name2}%23{id}/sections/season"
        return url
    else:
        split = player.split('#')
        name = split[0]
        id = split[1]
        url = f"https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/{name}%23{id}/sections/season"
        return url




"""Unused functions for now"""

"""
def getKnifeKills(url): #Gets Knife kills
    link = loadDriver(url)

    weapon_list = []

    weapon_finder = link.find_elements(By.CLASS_NAME, 'weapon-entry') #Find list of weapons

    for weapon in weapon_finder:
        weapon_list.append(weapon.text) #Aadd returned values to list

    #searches through weapon_list for the first item where the text before the newline character (\n) is 'Knife'.
    find_knife = next((item for item in weapon_list if item.split('\n')[0] == 'Knife'),None) 


    knife_kills = find_knife.split('\n')[1] #splits the find_knife string by newline characters, 1 being the position kills is

    link.quit()
    return knife_kills
"""


"""
#Keep for now, will not be used but is faster than reloading driver everytime for these stats
def getStats(url):
    driver = loadDriver(url)
    Variables
    data_list = [] # Initialize empty list to store data



    name_finder = driver.find_element(By.CLASS_NAME, 'user-name') #Finds username ***for now***
    name = name_finder.text #Stores name

    kd_finder = driver.find_elements(By.CLASS_NAME,'ov-stat-value') #Finds where KD is
    kd = kd_finder[0] #Limits element to KD
    kd_number = kd.text #Stores KD

    winp_finder = driver.find_elements(By.CLASS_NAME,'ov-stat-value') #Finds where win% is stored
    winp = winp_finder[1] #Limits element to win%
    winp_number = winp.text #stores win%'/////////

    agent_finder = driver.find_elements(By.CLASS_NAME, 'info-name') #Finds Top 3 agents
    top_agent = agent_finder[0] #Limits it to top agent
    top_agent_name = top_agent.text #stores top agent

    hs_percentage_finder = driver.find_elements(By.CLASS_NAME,'ov-stat-value') #Finds where HS% is stored
    hs_percentage = hs_percentage_finder[2] #Limits element to HS%
    hs_percentage_number = hs_percentage.text #stores HS%

    #Adding all calculated stats to data_list
    data_list.append(name) #Add name to list
    data_list.append(kd_number) #Add kd to list
    data_list.append(winp_number) #Add win% to list
    data_list.append(top_agent_name) #Add top agent to list
    data_list.append(hs_percentage_number) #Add HS% to list



    driver.quit() #Once all data is taken and stored into data_list, quit the driver
    return data_list

def getGameLinksForXYZ(url):
    driver = loadDriver(url)
    game_links = []
    get_match_links = driver.find_elements(By.CLASS_NAME, 'match-entry-link')

    for match in get_match_links:
        game_links.append(match.get_attribute('href'))
    
    game_links = game_links[:5]


    driver.quit()
    return game_links

def getStatsForOneGame(link):
    game = loadDriver(link) #Load driver with current link(XYZ player page)

    game_stats = [] #Create empty list for player game stats

    stats = game.find_elements(By.CLASS_NAME, 'value-title') #limit it container with stat values

    #Loop that gets the text from value-title, replaces the new line character and adds stat to stat list
    for stat in stats:
       stat = stat.text #Get the text
       stat = stat.replace("\n", " ") #Replace the new line character within the text with a space
       game_stats.append(stat) #Add stat game_stats

    game.quit()
    
    return game_stats #Return stats list to main


GROSS FUNCTIONS THAT DONT WORK PROPERLY
def getGameLinksForBlitz(url):
    driver  = loadDriver(url)
    game_links = []
    get_match_links = driver.find_elements(By.CLASS_NAME, 'match-link')

    for match in get_match_links:
        game_links.append(match.get_attribute('href'))
    game_links = game_links[:5]

    driver.quit()
    return game_links
"""

"""
def getAvgTeamWinPercentage(url): #Gets average win% per team based on the game link that was inserted
    driver = loadDriver(url)
    team_1_win_percentage_list = [] #team 1 win percentage list
    team_2_win_percentage_list = [] #Team 2 win percentage list
    player_list = [] #List to store all players in current match
    get_team_row = driver.find_elements(By.CLASS_NAME,'team__row-data-nick') #finds individual player names
    
    for player in get_team_row: #Loop to just have the player names and the Riot ID'S
        player = player.text
        player = player.replace('\n',' ')
        player = player.replace('#','')
        player_list.append(player) 
        
    print("Teams Created")
    team_1 = player_list[:5] #Creates team 1
    print(f"Team 1: {team_1}")
    team_2 = player_list[5:] #Creates team 2
    print(f"Team2: {team_2}")
    #Loop through team 1 and 2, create link using link outline,get overall stats for player, only get winp, convert to float, add to list
    for i in team_1:
        player = createPlayerLink(i)
        stats = getOverallStats(player)
        winp = stats[1]
        winp = winp.split(" ")[0]
        winp = winp.replace("%","")
        if winp == "N/A":
            pass
        else:
            winp = float(winp)
            team_1_win_percentage_list.append(winp)
    
    for i in team_2:
        player = createPlayerLink(i)
        stats = getOverallStats(player)
        winp = stats[1]
        winp = winp.split(" ")[0]
        winp = winp.replace("%","")
        if winp == "N/A":
            pass
        else:
            winp = float(winp)
            team_2_win_percentage_list.append(winp)
    
    #Finds the average win% for each team
    team_1_win_percentage_average = round(sum(team_1_win_percentage_list)/len(team_1_win_percentage_list))
    team_2_win_percentage_average = round(sum(team_2_win_percentage_list)/len(team_2_win_percentage_list))
    
    driver.quit()
    return team_1_win_percentage_average,team_2_win_percentage_average,team_1,team_2
"""
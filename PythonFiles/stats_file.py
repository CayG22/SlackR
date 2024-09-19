"""Libraries"""
from selenium import webdriver #Selenium -> webdriver: Used to connect web driver to program
from selenium.webdriver.chrome.service import Service #Selenium -> Service
from selenium.webdriver.chrome.options import Options #Selenium -> Options: Allows for custom options to be called
from selenium.webdriver.common.by import By #Selenium -> By: Allows for calls by specific variables from html code
from webdriver_manager.chrome import ChromeDriverManager #Webdriver_manager -> ChromeDriverManager: Allows for chrome driver to be ran
from selenium.common.exceptions import StaleElementReferenceException



"""Functionality functions"""
def loadDriver(url): #Loads driver
    """Selenium"""
    options = Options() #intialize option variable to class Options
    options.add_argument('--headless') #Take away window from being open on program run

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options) #Initializes driver var to chrome driver
    driver.get(url) #URL for what html page I want
    driver.implicitly_wait(10) #Makes driver wait 10 ms before doing anything: Allows for everything to load before accessing HTML elements

    return driver

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
def getOverallStats(link): #Gets overall stats and adds them to one tuple(Tuple for now)
    driver = loadDriver(link)
    driver.implicitly_wait(10)
    kd = getKD(driver)
    winp = getWinPercantage(driver)
    top_agent = getTopAgent(driver)
    headshot_percentage = getHeadShotPercentage(driver)
    driver.quit()
    return kd,winp,top_agent,headshot_percentage

def getKD(driver): #Gets KD
    kd = driver.find_element(By.CLASS_NAME, 'info-kd')
    kd = kd.text
    return kd

def getWinPercantage(driver): #Gets Win%
    winp = driver.find_element(By.CLASS_NAME, 'info-win-rate')
    winp = winp.text
    return winp

def getTopAgent(driver): #Gets top agent
    find_top_agent = driver.find_elements(By.CLASS_NAME, 'agent-info')
    top_agent = find_top_agent[0].text
    top_agent = top_agent.split('\n')[0]
    return top_agent

def getHeadShotPercentage(driver): #Gets headshot percentage
    find_hs_perc = driver.find_elements(By.CLASS_NAME, 'accuracy__path')
    hs_perc = find_hs_perc[1].text
    return hs_perc

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





"""Unused functions for now"""

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
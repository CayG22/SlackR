"""Libraries"""
from selenium import webdriver #Selenium -> webdriver: Used to connect web driver to program
from selenium.webdriver.chrome.service import Service #Selenium -> Service
from selenium.webdriver.chrome.options import Options #Selenium -> Options: Allows for custom options to be called
from selenium.webdriver.common.by import By #Selenium -> By: Allows for calls by specific variables from html code
from webdriver_manager.chrome import ChromeDriverManager #Webdriver_manager -> ChromeDriverManager: Allows for chrome driver to be ran
import time
"""Trying to decide if I want to strucutre by website list, or by function types"""

#Loads driver
def loadDriver(url):
    """Selenium"""
    options = Options() #intialize option variable to class Options
    options.add_argument('--headless') #Take away window from being open on program run

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options) #Initializes driver var to chrome driver
    driver.get(url) #URL for what html page I want
    driver.implicitly_wait(10) #Makes driver wait 10 ms before doing anything: Allows for everything to load before accessing HTML elements

    return driver


"""Functions to get overall stats"""
def getName(url):
    driver = loadDriver(url)
    name_finder = driver.find_element(By.CLASS_NAME, 'user-name')
    name = name_finder.text
    
    driver.quit()
    return name

def getKD(url):
    driver = loadDriver(url)

    find_KD = driver.find_elements(By.CLASS_NAME,'ov-stat-value')
    kd = find_KD[0].text
    
    driver.quit()
    return kd

def getWinPercantage(url):
    driver = loadDriver(url)

    find_winp = driver.find_elements(By.CLASS_NAME, 'ov-stat-value')
    winp = find_winp[1].text

    driver.quit()
    return winp

def getTopAgent(url):
    driver = loadDriver(url)

    find_top_agent = driver.find_elements(By.CLASS_NAME, 'info-name')
    top_agent = find_top_agent[0].text

    driver.quit()
    return top_agent

def getHeadShotPercentage(url):
    driver = loadDriver(url)

    find_hs_perc = driver.find_elements(By.CLASS_NAME, 'ov-stat-value')
    hs_perc = find_hs_perc[2].text

    driver.quit()
    return hs_perc

def getKnifeKills(url):
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


#Gets stats for one SINGLE GAME, uses strats.gg game page
def getStatsForOneGame(link): #Uses strats.gg
    game = loadDriver(link) #Load driver with strats.gg link
    stat_list = [] 
    
    stats = game.find_elements(By.CLASS_NAME, 'compare-table__row') #Find stats
    
    for stat in stats:
        stat = stat.text #Get text
        stat = stat.replace("\n"," ") #Replace new line character with space
        stat_list.append(stat) #Add stat to list
    
    game.quit() #close driver
    return stat_list #Return game stats

#Gets LAST FIVE GAMES PLAYED links, uses strats.gg overview page
def getGameLinksForStratsGG(link):
    strats = loadDriver(link) #Load driver
    game_list = [] 

    game_links = strats.find_elements(By.CSS_SELECTOR, "a.match") #a.match: match is the CSS selector, a is the anchor tag
    all_links = [link.get_attribute('href') for link in game_links] #Just get the links

    for href in all_links:
        game_list.append(href) #Add links to list
    
    strats.quit()
    return game_list[:5] #Return last give games played


"""Unused functions for now"""
#Keep for now, will not be used but is faster than reloading driver everytime for these stats
def getStats(url):
    driver = loadDriver(url)
    """Variables"""
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
"""
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
"""

"""GROSS FUNCTIONS THAT DONT WORK PROPERLY"""
def getGameLinksForBlitz(url):
    driver  = loadDriver(url)
    game_links = []
    get_match_links = driver.find_elements(By.CLASS_NAME, 'match-link')

    for match in get_match_links:
        game_links.append(match.get_attribute('href'))
    game_links = game_links[:5]

    driver.quit()
    return game_links
   



    
    
    
    

    
    
    




    



"""Libraries"""
from selenium import webdriver #Selenium -> webdriver: Used to connect web driver to program
from selenium.webdriver.chrome.service import Service #Selenium -> Service
from selenium.webdriver.chrome.options import Options #Selenium -> Options: Allows for custom options to be called
from selenium.webdriver.common.by import By #Selenium -> By: Allows for calls by specific variables from html code
from webdriver_manager.chrome import ChromeDriverManager #Webdriver_manager -> ChromeDriverManager: Allows for chrome driver to be ran
import time


def loadDriver(url):
    """Selenium"""
    options = Options() #intialize option variable to class Options
    options.add_argument('--headless') #Take away window from being open on program run

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options) #Initializes driver var to chrome driver
    driver.get(url) #URL for what html page I want
    driver.implicitly_wait(10) #Makes driver wait 10 ms before doing anything: Allows for everything to load before accessing HTML elements

    return driver


def getStats(url):

    """Variables"""
    data_list = [] # Initialize empty list to store data


    """Selenium"""
    options = Options() #intialize option variable to class Options
    options.add_argument('--headless') #Take away window from being open on program run

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options) #Initializes driver var to chrome driver
    driver.get(url) #URL for what html page I want
    driver.implicitly_wait(10) #Makes driver wait 10 ms before doing anything: Allows for everything to load before accessing HTML elements



    name_finder = driver.find_element(By.CLASS_NAME, 'user-name') #Finds username ***for now***
    name = name_finder.text #Stores name

    kd_finder = driver.find_elements(By.CLASS_NAME,'ov-stat-value') #Finds where KD is
    kd = kd_finder[0] #Limits element to KD
    kd_number = kd.text #Stores KD

    winp_finder = driver.find_elements(By.CLASS_NAME,'ov-stat-value') #Finds where win% is stored
    winp = winp_finder[1] #Limits element to win%
    winp_number = winp.text #stores win%

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



#Gets first deaths for a single game
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


def getGameLinksForXYZ(url):
    driver = loadDriver(url)
    game_links = []
    get_match_links = driver.find_elements(By.CLASS_NAME, 'match-entry-link')

    for match in get_match_links:
        game_links.append(match.get_attribute('href'))
    
    game_links = game_links[:5]


    driver.quit()
    return game_links



"""GROSS FUNCTIONS THAT DONT WORK PROPERLY"""
"""Algo needs work, no way to know which one is first deaths..."""
def getFirstDeathsForOneGame(link):
    game = loadDriver(link)
    first_deaths = []
    stats = []
    stat_number = game.find_elements(By.CLASS_NAME, 'type-body2.left')
    stat_name = game.find_elements(By.CLASS_NAME, 'type-caption.row-name')

    for name,number in zip(stat_name,stat_number):
        stats.append((name.text,number.text))
    
    game.quit()
    return stats






def getGameLinksForBlitz(url):
    driver  = loadDriver(url)
    game_links = []
    get_match_links = driver.find_elements(By.CLASS_NAME, 'match-link')

    for match in get_match_links:
        game_links.append(match.get_attribute('href'))
    game_links = game_links[:5]

    driver.quit()
    return game_links
   



    
    
    
    

    
    
    




    



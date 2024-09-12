"""Libraries"""
from selenium import webdriver #Selenium -> webdriver: Used to connect web driver to program
from selenium.webdriver.chrome.service import Service #Selenium -> Service
from selenium.webdriver.chrome.options import Options #Selenium -> Options: Allows for custom options to be called
from selenium.webdriver.common.by import By #Selenium -> By: Allows for calls by specific variables from html code
from webdriver_manager.chrome import ChromeDriverManager #Webdriver_manager -> ChromeDriverManager: Allows for chrome driver to be ran


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
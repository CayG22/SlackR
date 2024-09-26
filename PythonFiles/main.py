"""
    main.py
    Cayden Garcia
    Fall 2024 - Advanced Software Engineering
    Will call all main functions of SlackR
"""
from stats_file import findRoundOutcome,getAvgTeamWinPercentage,calculateAntiThrifties,getGameLinksForBlitzGG,findWinOrLoss,findEconomyAverage,loadDriver,getKnifeKills, getStatsForOneGame,getStatsForOneGame,getKD,getWinPercantage,getTopAgent,getHeadShotPercentage, getGameLinksForStratsGG, getOverallStats, get149DamageDone


print("Hello, and welcome to SlackR\n\n")
url = "https://valorantstats.xyz/stats/profile/OC%20Jrmzie-410/weapons?actId=all&gameMode=all" #will need for url outline
url2 = "https://www.strats.gg/valorant/stats/SEN%20curry%23lisa/overview" #Overview page for game links for Strats.gg, will need for url outline
url3 = "https://www.strats.gg/valorant/stats/canezerra%23LVgod/overview"
weapons_url = "https://www.strats.gg/valorant/stats/twitch%20nightz1x%23aim/weapons" #Weapons page for Strats.gg, 149DamageDone. Will need for url outline
url4 = "https://blitz.gg/valorant/match/sen%20curry-lisa/292f58db-4c17-89a7-b1c0-ba988f0e9d98/7963a8e3-926e-4fe6-a9bb-12405e7d96d7"
blitz_overview = "https://blitz.gg/valorant/profile/sen%20curry-lisa"
win_perc_algo_url = "https://www.strats.gg/valorant/stats/SEN%20curry%23lisa/match/d76ad609-12dc-4a26-aa8c-ef3e92dde1b9"

"""
user_input = input("Please enter your username, then a space, then your ID (No pound symbol):")
#Condition to see if username is either one part or two, could change to for loop to account for how many spaces in the first place but whatever for now
if user_input.count(" ") == 1:
    username = user_input.split(' ')[0]
    id = user_input.split(' ')[1]
    test_url = f"https://www.strats.gg/valorant/stats/{username}%23{id}/overview"
elif user_input.count(" ") == 2:
    first_part = user_input.split(' ')[0]
    second_part = user_input.split(' ')[1]
    id = user_input.split(' ')[2]
    test_url = f"https://www.strats.gg/valorant/stats/{first_part}%20{second_part}%23{id}/overview"

print("Now getting your stats...")
"""
findRoundOutcome(win_perc_algo_url)
#getAvgTeamWinPercentage(win_perc_algo_url)
#print(getOverallStats(url2))
#get149DamageDone(weapons_url)
#getAntiThrifties(url4)
#findWinOrLoss(blitz_overview)
#getGameLinksForBlitzGG(blitz_overview)
#calculateAntiThrifties(blitz_overview)



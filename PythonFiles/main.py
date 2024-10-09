"""
    main.py
    Cayden Garcia
    Fall 2024 - Advanced Software Engineering
    Will call all main functions of SlackR
"""
from stats_file import calculateRoundWinPercentage,create_players,loadWeaponStats,loadCharacterStats,createAPIPlayerLink,getPlayersInGame,loadPlayerProfile,assignTeam,loadGame,getKillsPerRound,findRoundOutcome,getAvgTeamWinPercentage,calculateAntiThrifties,getGameLinksForBlitzGG,findWinOrLoss,findEconomyAverage,loadDriver,getKnifeKills, getStatsForOneGame,getStatsForOneGame,getKD,getWinPercentage,getTopAgent,getHeadShotPercentage, getGameLinksForStratsGG, getOverallStats, get149DamageDone
from class_file import *

print("Hello, and welcome to SlackR\n\n")
#url = "https://valorantstats.xyz/stats/profile/OC%20Jrmzie-410/weapons?actId=all&gameMode=all" #will need for url outline
#url2 = "https://www.strats.gg/valorant/stats/SEN%20curry%23lisa/overview" #Overview page for game links for Strats.gg, will need for url outline
#url3 = "https://www.strats.gg/valorant/stats/canezerra%23LVgod/overview"
#weapons_url = "https://www.strats.gg/valorant/stats/twitch%20nightz1x%23aim/weapons" #Weapons page for Strats.gg, 149DamageDone. Will need for url outline
#url4 = "https://blitz.gg/valorant/match/sen%20curry-lisa/292f58db-4c17-89a7-b1c0-ba988f0e9d98/7963a8e3-926e-4fe6-a9bb-12405e7d96d7"
#blitz_overview = "https://blitz.gg/valorant/profile/sen%20curry-lisa"
#win_perc_algo_url = "https://www.strats.gg/valorant/stats/SEN%20curry%23lisa/match/d76ad609-12dc-4a26-aa8c-ef3e92dde1b9"
game_url = "https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/100T%20Asuna%231111/matches/1cca6e91-ce8d-498d-96cf-5ace1f250ab7" #Direct API call
#player_url = "https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/PA1NT%23Peak/sections/season"
#player_character_url = "https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/PA1NT%23Peak/sections/characters"
#weapons_file_url = "https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/PA1NT%23Peak/sections/weapons"
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


game = loadGame(game_url)
players = create_players(game)
game_money_list = [] #List we are passing in to calculate the win%
round_outcomes = findRoundOutcome(game)


for player in players:
    round_money = player.calculate_money(game)
    #player.display_info()
    game_money_list.append(round_money)



players[0] = calculateRoundWinPercentage(player,game_money_list,round_money,round_outcomes)
    

































#x = loadWeaponStats(weapons_file_url)
#getKnifeKills(x)
#x = loadCharacterStats(player_character_url)
#top_agent = getTopAgent(x)
#player = loadPlayerProfile(player_url)
#getHeadShotPercentage(player)
#kd = getKD(player)
#game = loadGame(game_url) #Load game I am looking at
#players = getPlayersInGame(game) #Get all the names in that game
#winp_list = getAvgTeamWinPercentage(players)
#game = loadGame(game_url)
#kills_per_round = findRoundOutcome(game)
#findRoundOutcome(win_perc_algo_url)
#getAvgTeamWinPercentage(win_perc_algo_url)
#print(getOverallStats(url2))
#get149DamageDone(weapons_url)
#getAntiThrifties(url4)
#findWinOrLoss(blitz_overview)
#getGameLinksForBlitzGG(blitz_overview)
#calculateAntiThrifties(blitz_overview)



"""
    main.py
    Cayden Garcia
    Fall 2024 - Advanced Software Engineering
    Will call all main functions of SlackR
"""
from stats_file import getStats,getKnifeKills, getStatsForOneGame,getGameLinksForBlitz, getGameLinksForXYZ,getStatsForOneGame, getName,getKD,getWinPercantage,getTopAgent,getHeadShotPercentage


print("Hello, and welcome to SlackR\n\n")
url = "https://valorantstats.xyz/stats/profile/SEN%20curry-lisa?actId=all&gameMode=competitive" #Will need for url outline
url2 = "https://valorantstats.xyz/stats/profile/OC%20Jrmzie-410/weapons?actId=all&gameMode=all" #will need for url outline
url3 = "https://blitz.gg/valorant/match/sen%20curry-lisa/292f58db-4c17-89a7-b1c0-ba988f0e9d98/2e7155e0-e7ed-42c2-a78c-b076d9c00090"
url4 = "https://blitz.gg/valorant/profile/sen%20curry-lisa?queue=competitive"
url5 = "https://www.strats.gg/valorant/stats/SEN%20curry%23lisa/match/2e7155e0-e7ed-42c2-a78c-b076d9c00090"

#name = getName(url)
#print(name)
#kd = getKD(url)
#print(kd)
#winp = getWinPercantage(url)
#print(winp)
#top_agent = getTopAgent(url)
#print(top_agent)
#headshot_percentage = getHeadShotPercentage(url)
#print(headshot_percentage)

stats = getStatsForOneGame(url5)
print(stats)


#stats = getStats(url)
#knife_kills = getKnifeKills(url2)
#game_links = getGameLinksForXYZ(url)
#game_stats = getStatsForOneGame(game_links[0])
#game_links = getGameLinksForBlitz(url4) NOOOOOOO, works fine but don't need rn
#first_deaths = getFirstDeathsForOneGame(game_links[0]) Grabs stats but can't tell which one is right, gonna try diff website
#header_list = ["Name","KD", "Win %","Top Agent","HS %"] # List to store all headers I want, 
                                                        #just make sure the data being pulled is in the same position as the list position
#row_ = 1 #integer for accesing specific row
#column_ = 1 #integer for accessing specific column













"""pyxl
workbook = openpyxl.Workbook() #opens workbook 
sheet = workbook.active #sets workbook to active
#for loop to store data into a new column on a single row, must enumerate header_list since 'i' refers to each element not the index
for i, header in enumerate(header_list):
    sheet.cell(row = row_, column = column_, value = header_list[i])
    column_ += 1
#storing data into spots(CREATE FOR LOOP)  
sheet.cell(row=2,column=1,value = data_list[0]) #Store name into (2,1)
sheet.cell(row=2,column=2,value = data_list[1]) #Store KD into (2,2)
sheet.cell(row=2,column=3,value = data_list[2]) #Store Win% into (2,3)
sheet.cell(row=2,column=4,value = data_list[3]) #Store Top agent into (2,4)
sheet.cell(row=2,column=5,value = data_list[4]) #Store Top agent into (2,4)

workbook.save("SlackR_stats.xlsx") #Saves file to workbook
print("Data has been saved to SlackR_stats.xlsx") #Ouput to show program is done running
"""
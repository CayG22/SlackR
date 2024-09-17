"""
    main.py
    Cayden Garcia
    Fall 2024 - Advanced Software Engineering
    Will call all main functions of SlackR
"""
from stats_file import getKnifeKills, getStatsForOneGame,getStatsForOneGame,getKD,getWinPercantage,getTopAgent,getHeadShotPercentage, getGameLinksForStratsGG, getOverallStats


print("Hello, and welcome to SlackR\n\n")
url = "https://valorantstats.xyz/stats/profile/OC%20Jrmzie-410/weapons?actId=all&gameMode=all" #will need for url outline
url2 = "https://www.strats.gg/valorant/stats/SEN%20curry%23lisa/overview" #Overview page for game links for Strats.gg, will need for url outline










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
"""
    main.py
    Cayden Garcia
    Fall 2024 - Advanced Software Engineering
    Will call all main functions of SlackR
"""
from stats_file import getStats,getKnifeKills,getFirstDeaths


print("Hello, and welcome to SlackR\n\n")
url = "https://valorantstats.xyz/stats/profile/SEN%20curry-lisa?actId=all&gameMode=all"
url2 = "https://valorantstats.xyz/stats/profile/OC%20Jrmzie-410/weapons?actId=all&gameMode=all"
url3 = "https://blitz.gg/valorant/match/sen%20curry-lisa/292f58db-4c17-89a7-b1c0-ba988f0e9d98/2e7155e0-e7ed-42c2-a78c-b076d9c00090"

#stats = getStats(url)
#knife_kills = getKnifeKills(url2)
first_deaths = getFirstDeaths(url3)
#print(stats)
#print(f"Knife kills: {knife_kills}")
print(first_deaths)
header_list = ["Name","KD", "Win %","Top Agent","HS %"] # List to store all headers I want, 
                                                        #just make sure the data being pulled is in the same position as the list position
row_ = 1 #integer for accesing specific row
column_ = 1 #integer for accessing specific column













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
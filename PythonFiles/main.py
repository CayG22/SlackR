"""
    main.py
    Cayden Garcia
    Fall 2024 - Advanced Software Engineering
    Will call all main functions of SlackR
"""
from stats import getStats


print("Hello, and welcome to SlackR\n\n")
url = "https://valorantstats.xyz/stats/profile/SEN%20curry-lisa?actId=all&gameMode=all"

stats = getStats(url)

print(stats)


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
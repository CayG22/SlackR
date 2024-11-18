"""
    main.py
    Cayden Garcia
    Fall 2024 - Advanced Software Engineering
    Will call all main functions of SlackR
"""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
import pandas as pd
from tkinter import filedialog, messagebox, ttk

from stats_file import *  # Import all relevant functions
from class_file import *  # Import any classes used in stats

print("Hello, and welcome to SlackR\n\n")
#url = "https://valorantstats.xyz/stats/profile/OC%20Jrmzie-410/weapons?actId=all&gameMode=all" #will need for url outline
#url2 = "https://www.strats.gg/valorant/stats/SEN%20curry%23lisa/overview" #Overview page for game links for Strats.gg, will need for url outline
#url3 = "https://www.strats.gg/valorant/stats/canezerra%23LVgod/overview"
#weapons_url = "https://www.strats.gg/valorant/stats/twitch%20nightz1x%23aim/weapons" #Weapons page for Strats.gg, 149DamageDone. Will need for url outline
#url4 = "https://blitz.gg/valorant/match/sen%20curry-lisa/292f58db-4c17-89a7-b1c0-ba988f0e9d98/7963a8e3-926e-4fe6-a9bb-12405e7d96d7"
#blitz_overview = "https://blitz.gg/valorant/profile/sen%20curry-lisa"
#win_perc_algo_url = "https://www.strats.gg/valorant/stats/SEN%20curry%23lisa/match/d76ad609-12dc-4a26-aa8c-ef3e92dde1b9"
game_url = "https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/100T%20Asuna%231111/matches/1cca6e91-ce8d-498d-96cf-5ace1f250ab7" #Direct API call
game_url_2 = "https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/469%20ion2x%231love/matches/e8d6a0ed-69ef-40d7-bca8-7701a627f5e5"
#player_url = "https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/PA1NT%23Peak/sections/season"
#player_character_url = "https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/PA1NT%23Peak/sections/characters"
#weapons_file_url = "https://api.strats.gg/internal/api/v1/games/valorant/accounts/riot/PA1NT%23Peak/sections/weapons"
#test_player = Player(player_file,character_file,weapon_file)

def create_input_layout():
    #Layout for input page(USER MUST HAVE "NAME #ID" i.e KAGS #7158)
    layout = [
        [sg.Text(text = "Please enter your Riot Username and ID(Name,Space,ID)",background_color=sg.theme_background_color()),sg.InputText()],
        [sg.Button(button_text = "Load Profile", button_color=sg.theme_background_color()), sg.Button("Close", button_color=sg.theme_background_color())]

    ]
    return layout

def create_home_page_layout(current_player,recent_matches):
    #Data for current players overall stats
    headers = ["Stat", "Number"]
    data = [
        ["KD", current_player.kd],
        ["Win Percentage", current_player.winp],
        ["Top Agent", current_player.top_agent],
        ["Headshot Percentage", current_player.headshot_percentage],
        ["Clutches", current_player.clutches],
        ["First Kills", current_player.first_kills],
        ["First Deaths", current_player.first_deaths],
        ["Knife Kills", current_player.knife_kills],
        ["149 Damage Done", current_player.one_four_nine_damage_done],
        ["Rank", current_player.rank],
        ["Archetype", current_player.archetype],
    ]
    
    #Data for last five games player has played
    game_headers = ["Rank", "Map Name", "Agent"]
    game_data = [
        [recent_matches.current_rank[0], recent_matches.names[0], recent_matches.agents_played[0]],
        [recent_matches.current_rank[1], recent_matches.names[1], recent_matches.agents_played[1]],
        [recent_matches.current_rank[2], recent_matches.names[2], recent_matches.agents_played[2]],
        [recent_matches.current_rank[3], recent_matches.names[3], recent_matches.agents_played[3]],
        [recent_matches.current_rank[4], recent_matches.names[4], recent_matches.agents_played[4]]

    ]
    
    #Layout for home page
    tab_layout_1 = [
        [sg.Text(f"Player Profile: {current_player.name}", font=("Helvetica", 16), justification="center")],
        [sg.Table(values=data, expand_y = True, row_height = 40, headings=headers, auto_size_columns=True, justification="left", key="-TABLE-"), sg.Image(source = f"rankImages\{current_player.rank}.png", size = (500,500))],
        [sg.Button("Close")]
    ]
    tab_layout_2 = [
        [sg.Text(text = "Choose a game", justification="center")],
        [sg.Table(values = game_data, row_height= 50, headings=game_headers, auto_size_columns= True,expand_x= True,justification="center",key="GAME_TABLE", enable_events=True)]
    ]

    layout = [
        [sg.TabGroup([[sg.Tab("Overview",tab_layout_1), sg.Tab("Games", tab_layout_2)]])]
    ]

    return layout

def create_game_page_layout(red_team,blue_team,red_econ,blue_econ):
    
    #Red team stats
    red_data = [
        [red_team[0].agent,red_team[0].name,red_team[0].kills,red_team[0].deaths,red_team[0].assists,red_team[0].hs_perc,red_team[0].multi_kills],
        [red_team[1].agent,red_team[1].name,red_team[1].kills,red_team[1].deaths,red_team[1].assists,red_team[1].hs_perc,red_team[1].multi_kills],
        [red_team[2].agent,red_team[2].name,red_team[2].kills,red_team[2].deaths,red_team[2].assists,red_team[2].hs_perc,red_team[2].multi_kills],
        [red_team[3].agent,red_team[3].name,red_team[3].kills,red_team[3].deaths,red_team[3].assists,red_team[3].hs_perc,red_team[3].multi_kills],
        [red_team[4].agent,red_team[4].name,red_team[4].kills,red_team[4].deaths,red_team[4].assists,red_team[4].hs_perc,red_team[4].multi_kills]
    ]
    
    #blue team stats
    blue_data = [
        [blue_team[0].agent,blue_team[0].name,blue_team[0].kills,blue_team[0].deaths,blue_team[0].assists,blue_team[0].hs_perc,blue_team[0].multi_kills],
        [blue_team[1].agent,blue_team[1].name,blue_team[1].kills,blue_team[1].deaths,blue_team[1].assists,blue_team[1].hs_perc,blue_team[1].multi_kills],
        [blue_team[2].agent,blue_team[2].name,blue_team[2].kills,blue_team[2].deaths,blue_team[2].assists,blue_team[2].hs_perc,blue_team[2].multi_kills],
        [blue_team[3].agent,blue_team[3].name,blue_team[3].kills,blue_team[3].deaths,blue_team[3].assists,blue_team[3].hs_perc,blue_team[3].multi_kills],
        [blue_team[4].agent,blue_team[4].name,blue_team[4].kills,blue_team[4].deaths,blue_team[4].assists,blue_team[4].hs_perc,blue_team[4].multi_kills]
    ]

    #Layout for page
    headers = ['Agent','Name','Kills', 'Deaths', 'Assists', 'HS%',"Multi-Kills"]
    layout = [
        [sg.Table(values = red_data, headings=headers, num_rows=5,row_height=30,auto_size_columns=True, key='RED_TABLE',enable_events=True, background_color='#f28282')],
        [sg.Table(values=blue_data, headings = headers,num_rows=5,row_height=30,auto_size_columns=True,key = 'BLUE_TABLE',enable_events=True,background_color='#82a7f2')]
    ]

    return layout

def create_secondary_player_layout(current_player):
    data = [
        ["KD", current_player.kd],
        ["Win Percentage", current_player.winp],
        ["Top Agent", current_player.top_agent],
        ["Headshot Percentage", current_player.headshot_percentage],
        ["Clutches", current_player.clutches],
        ["First Kills", current_player.first_kills],
        ["First Deaths", current_player.first_deaths],
        ["Knife Kills", current_player.knife_kills],
        ["149 Damage Done", current_player.one_four_nine_damage_done],
        ["Rank", current_player.rank],
        ["Archetype", current_player.archetype],
    ]  

    #Layout
    headers = ["Stat", "Number"]
    layout = [
        [sg.Text(f"Player Profile: {current_player.name}", font=("Helvetica", 16), justification="center")],
        [sg.Table(values=data, expand_y = True, row_height = 40, headings=headers, auto_size_columns=True, justification="left", key="-TABLE-"), sg.Image(source = f"rankImages\{current_player.rank}.png", size = (500,500))],
        [sg.Button("Close")]
    ]

    return layout

def main():
    layout = create_input_layout()
    theme = sg.theme("LightPurple")
    window = sg.Window("SlackR", layout)
    
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event =="Close":
            break
        if event == "Load Profile":
            player_link = createAPIPlayerLink(values[0])
            weapon_link = createAPIWeaponLink(values[0])
            character_link = createAPICharacterLink(values[0])
            recent_matches_link = createAPIMatchesLink(values[0])

            player_file = loadPlayerProfile(player_link)
            weapon_file = loadWeaponStats(weapon_link)
            character_file = loadCharacterStats(character_link)
            recent_matches_file = loadRecentMatches(recent_matches_link)

            recent_matches = Matches(recent_matches_file)
            current_player = Player(values[0],player_file,character_file,weapon_file)

            current_player.export_to_excel()
            window.close()
            home_layout = create_home_page_layout(current_player,recent_matches)
            home_window = sg.Window("SlackR-Home Page", home_layout)

            while True:
                home_event,values = home_window.read()
                if home_event == sg.WINDOW_CLOSED or home_event == "Close":
                    break


                if home_event == "GAME_TABLE":
                    selected = values["GAME_TABLE"] #Returns what number row was selected in pos 0
                    if selected[0] == 0:
                        game_link = createAPIGameLink(current_player.name, recent_matches.gameAPILink[0])
                    elif selected[0] == 1:
                        game_link = createAPIGameLink(current_player.name, recent_matches.gameAPILink[1])
                    elif selected[0] == 2:
                        game_link = createAPIGameLink(current_player.name, recent_matches.gameAPILink[2])
                    elif selected[0] == 3:
                        game_link = createAPIGameLink(current_player.name, recent_matches.gameAPILink[3])
                    elif selected[0] == 4:
                        game_link = createAPIGameLink(current_player.name, recent_matches.gameAPILink[4])
                    else:
                        print("Something went wrong, please try again")
                    
                    game_file = loadGame(game_link)
                    game = Game(game_file)
                    red_team = []
                    blue_team = []
                    
                    for i in range(10):
                        current_teammate = Teamate(game_file,game.players[i])
                        if current_teammate.team == 'Red':
                            red_team.append(current_teammate)
                        else:
                            blue_team.append(current_teammate)
                    
                    econ = Economy(game_file,game.red_team,game.blue_team)

                    game_layout = create_game_page_layout(red_team,blue_team,econ.red_economy,econ.red_economy)
                    game_window = sg.Window("Game Page",game_layout)

                    while True:
                        game_event,player_values = game_window.read()
                        if game_event == sg.WINDOW_CLOSED:
                            break
                        
                        if game_event == "RED_TABLE":
                            player_selected = player_values['RED_TABLE']
                            if player_selected[0] == 0:
                                new_player = red_team[0].name
                            elif player_selected[0] == 1:
                                new_player = red_team[1].name
                            elif player_selected[0] == 2:
                                new_player = red_team[2].name
                            elif player_selected[0] == 3:
                                new_player = red_team[3].name
                            elif player_selected[0] == 4:
                                new_player = red_team[4].name
                        elif game_event == "BLUE_TABLE":
                            player_selected = player_values['BLUE_TABLE']
                            if player_selected[0] == 0:
                                new_player = blue_team[0].name
                            elif player_selected[0] == 1:
                                new_player = blue_team[1].name
                            elif player_selected[0] == 2:
                                new_player = blue_team[2].name
                            elif player_selected[0] == 3:
                                new_player = blue_team[3].name
                            elif player_selected[0] == 4:
                                new_player = blue_team[4].name
                        new_player = new_player.replace("#"," #")
                        
                        new_player_player_link = createAPIPlayerLink(new_player)
                        new_player_weapon_link = createAPIWeaponLink(new_player)
                        new_player_character_link = createAPICharacterLink(new_player)
                        
                        new_player_player_file = loadPlayerProfile(new_player_player_link)
                        new_player_weapon_file = loadWeaponStats(new_player_weapon_link)
                        new_player_character_file = loadCharacterStats(new_player_character_link)

                        try:
                            secondary_player = Player(new_player,new_player_player_file,new_player_character_file,new_player_weapon_file)
                            secondary_player.export_to_excel()
                            
                            secondary_home_layout = create_secondary_player_layout(secondary_player)
                            secondary_home_window = sg.Window(f"{secondary_player.name} Overiview",secondary_home_layout)
                            
                            while True:
                                secondary_home_event,_ = secondary_home_window.read()
                                if secondary_home_event == sg.WINDOW_CLOSED:
                                    break
                        except Exception as e:
                            print(e)
                            sg.popup("Profile is private...")



                    game_window.close()
            home_window.close()
            break



if __name__ == "__main__":
    main()


"""MAIN START
# Main Application Window
class SlackRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SlackR - Valorant Stat Tracker")
        self.geometry("1000x700")
        
        # Container frame for pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        
        self.frames = {}
        for F in (PlayerEntryPage,OverviewPage, GamePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show Overview page on startup
        self.show_frame("PlayerEntryPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

#Player Entry Page
class PlayerEntryPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        #Title label
        title_label = tk.Label(self,text="Enter Player Information", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=10)

        #Username and ID entry fields
        user_label = tk.Label(self,text="Enter(Username,space,id):")
        user_label.pack()
        self.user_entry = tk.Entry(self)
        self.user_entry.pack()

        #Submit button
        submit_button = ttk.Button(self,text="Submit",command = self.on_submit)
        submit_button.pack(pady=20)

    def on_submit(self):
        user = self.user_entry.get()
        print(user)
        
        api_player_link = createAPIPlayerLink(user)
        api_weapon_link = createAPIWeaponLink(user)
        api_character_link = createAPICharacterLink(user)
        
        if " " in api_player_link:
            api_player_link = api_player_link.replace(" ", "")
        if " " in api_character_link:
            api_character_link = api_character_link.replace(" ", "")    
        if " " in api_weapon_link:
            api_weapon_link = api_weapon_link.replace(" ", "")
        
        print("Generated api player link:",api_player_link)
        print("Generated api weapon link:",api_weapon_link)
        print("Generated api character link:",api_character_link)
        player_page = loadPlayerProfile(api_player_link)
        weapon_page = loadWeaponStats(api_weapon_link)
        character_page = loadCharacterStats(api_character_link)

        self.controller.frames["OverviewPage"].load_overview_stats(player_page,weapon_page,character_page)
        self.controller.show_frame("OverviewPage")

# Overview Page
class OverviewPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Title Label
        title_label = tk.Label(self, text="SlackR Overview", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=10)
        
        # Stats Display Section
        stats_frame = tk.Frame(self)
        stats_frame.pack(pady=20)
        
        # Labels for displaying real-time stats
        self.kd_label = tk.Label(stats_frame, text="K/D Ratio: Loading...", font=("Helvetica", 14))
        self.win_perc_label = tk.Label(stats_frame, text="Win Percentage: Loading...", font=("Helvetica", 14))
        self.top_agent_label = tk.Label(stats_frame, text="Top Agent: Loading..", font=("Helvetica", 14))
        self.knife_kills_label = tk.Label(stats_frame, text="Knife Kills: Loading...", font=("Helvetica", 14))
        self.hs_perc_label = tk.Label(stats_frame, text="Headshot %: Loading...", font=("Helvetica", 14))
        #self.one_four_nine_dam_done_label = tk.Label(stats_frame, text="149 Damage done: Loading...", font=("Helvetica", 14))

        self.rank_label = tk.Label(stats_frame, text="Rank: Loading...", font=("Helvetica", 14))
        self.archetype_label = tk.Label(stats_frame, text="Archetype: Loading...", font=("Helvetica", 14))
        
        self.kd_label.pack(anchor="w")
        self.win_perc_label.pack(anchor="w")
        self.top_agent_label.pack(anchor="w")
        self.knife_kills_label.pack(anchor="w")
        self.hs_perc_label.pack(anchor="w")
        #self.one_four_nine_dam_done_label.pack(anchor="w")
        self.rank_label.pack(anchor="w")
        self.archetype_label.pack(anchor="w")
        
        # Load Stats Button
        load_stats_button = ttk.Button(self, text="Load Stats", command=self.load_overview_stats)
        load_stats_button.pack(pady=10)
        
        # Navigate to Game Page
        game_button = ttk.Button(self, text="Go to Game Page", command=lambda: controller.show_frame("GamePage"))
        game_button.pack(pady=10)

    def load_overview_stats(self,player_page,weapon_page,character_page):
        # Retrieve stats from your functions
        # Replace 'player' with appropriate data from create_players or loadGame
        kd_ratio = getKD(player_page)
        win_perc = getWinPercentage(player_page)
        top_agent = getTopAgent(character_page)
        knife_kills = getKnifeKills(weapon_page)
        hs_perc = getHeadShotPercentage(player_page)
        
        # Update labels with retrieved stats
        self.kd_label.config(text=f"K/D Ratio: {kd_ratio}")
        self.win_perc_label.config(text=f"Win Percentage: {win_perc}%")
        self.top_agent_label.config(text=f"Top agent: {top_agent}")
        self.knife_kills_label.config(text=f"Knife Kills: {knife_kills}")
        self.hs_perc_label.config(text=f"Headshot Percentage: {hs_perc}%")
        self.rank_label.config(text=f"Rank: Gold 3")  # Update with real data
        self.archetype_label.config(text=f"Archetype: Duelist")  # Update with real data

# Game Page
class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Title Label
        title_label = tk.Label(self, text="SlackR Game Stats", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=10)
        
        # Create a frame for player stats and graph
        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack(pady=20)

        # Left Frame for Player Stats
        self.player_stats_frame = tk.Frame(self.stats_frame)
        self.player_stats_frame.pack(side=tk.LEFT, padx=(10, 20))

        # Right Frame for Plot Area
        self.plot_frame = tk.Frame(self.stats_frame)
        self.plot_frame.pack(side=tk.RIGHT)

        # Load Game Stats Button
        load_game_button = ttk.Button(self, text="Load Game Stats", command=self.load_game_stats)
        load_game_button.pack(pady=10)
        
        # Back to Overview Button
        overview_button = ttk.Button(self, text="Back to Overview", command=lambda: controller.show_frame("OverviewPage"))
        overview_button.pack(pady=10)

        # Variables for dragging
        self.is_dragging = False
        self.start_x = 0
        self.start_y = 0
        self.canvas = None  # Store the canvas for plotting

    def load_game_stats(self):
        # Call functions to retrieve game stats
        game = loadGame(game_url_2)
        match_info = create_match(game)
        players = create_players(game)
        round_outcomes = findRoundOutcome(game)
        teams = assignTeam(game)

        match_info.get_map_name(game)
        #self.display_map_image(match_info)
        # Game money list calculation
        game_money_list = []
        for player in players:
            player.get_stats(game)
            round_money = player.calculate_money(game)
            game_money_list.append(round_money)

        # Calculate win percentages
        red_team_win_percentage_list = []
        blue_team_win_percentage_list = []
        for i, player in enumerate(players): 
            x = calculatePlayerRoundWinPercentage(player, game_money_list, game_money_list[i], round_outcomes)
            if player.team == "Blue":
                blue_team_win_percentage_list.append(x)
            elif player.team == "Red":
                red_team_win_percentage_list.append(x)

        # Calculate cumulative win percentage
        combined_red_team_percentage_list = [sum(values) for values in zip(*red_team_win_percentage_list)]
        combined_blue_team_percentage_list = [sum(values) for values in zip(*blue_team_win_percentage_list)]
        
        blue_team_starting, red_team_starting = getAvgTeamWinPercentage(getPlayersInGame(game))
        blue_team_starting /= 100
        red_team_starting /= 100
        blue_team_cumulative = np.cumsum([blue_team_starting] + combined_blue_team_percentage_list)
        red_team_cumulative = np.cumsum([red_team_starting] + combined_red_team_percentage_list)

        rounds = list(range(0, len(combined_red_team_percentage_list) + 1))

        # Plotting
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(rounds, blue_team_cumulative, label="Blue Team Performance", marker="o", color="b")
        ax.plot(rounds, red_team_cumulative, label="Red Team Performance", marker="x", color="r")
        
        # Set y limits and add a bit of padding
        ax.set_ylim(0, 10.0)  # Slightly above 1 to keep lines visible
        ax.set_xlim(left=0, right=len(rounds)-1)  # Ensure x-axis covers all rounds

        # Set labels and title
        ax.set_xlabel("Rounds")
        ax.set_ylabel("Win %")
        ax.set_title("Team Performance Over Rounds")
        ax.legend()

        # Adjust layout to prevent clipping of tick-labels
        plt.tight_layout()

        # Embed the plot in Tkinter
        for widget in self.plot_frame.winfo_children():
            widget.destroy()  # Clear previous plots if any
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Make canvas fill the available space

        # Connect mouse events for dragging
        self.cid_press = fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

        # Display player stats
        self.display_player_stats(players)



    def on_press(self, event):
        if event.button == 1:  # Left mouse button
            self.is_dragging = True
            self.start_x = event.xdata
            self.start_y = event.ydata

    def on_release(self, event):
        if event.button == 1:  # Left mouse button
            self.is_dragging = False

    def on_motion(self, event):
        if self.is_dragging:
            ax = self.canvas.figure.axes[0]
            if event.xdata is None or event.ydata is None:  # Ignore if mouse is outside axes
                return
            dx = self.start_x - event.xdata
            dy = self.start_y - event.ydata
            
            # Update limits based on drag
            ax.set_xlim(ax.get_xlim()[0] + dx, ax.get_xlim()[1] + dx)
            ax.set_ylim(ax.get_ylim()[0] + dy, ax.get_ylim()[1] + dy)
            
            self.canvas.draw()

    def display_player_stats(self, players):
        # Clear previous player stats
        for widget in self.player_stats_frame.winfo_children():
            widget.destroy()
        for player in players:
            name  = player.name
            kills = player.kills
            deaths = player.deaths
            assists = player.assists
            headshot_percentage = player.head_shot_perc
            #print(name,kills,deaths,assists)
            player_label = tk.Label(self.player_stats_frame, text=f"Name: {name}, Kills: {kills}, Deaths: {deaths}, Assists: {assists}, HS%: {headshot_percentage}%")
            player_label.pack(anchor='w')  # Align to the left
    
    def display_map_image(self, match):
        # Load image
        name = match.name
        image_path = f"map_images\{name}.jpg"

        # Create label to display image
        img = Image.open(image_path)
        img = img.resize((800, 200), Image.LANCZOS)  # Optional, for high-quality resizing
        self.map_image = ImageTk.PhotoImage(img)  # Keep a reference of the image

        image_label = tk.Label(self.master, image=self.map_image)
        image_label.grid(row=0, column=0, padx=10, pady=10)  # Use grid instead of pack



# Run Application
if __name__ == "__main__":
    app = SlackRApp()
    app.mainloop()

"""
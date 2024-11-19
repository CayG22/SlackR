from stats_file import *
from utils import openJsonFile
import pandas as pd
from rank_config import ARCHETYPES, RANKS #For rank and archetype assignment
import os


class Player: #For current player that is looking at his/her stats
    def __init__(self,name,player_file,character_file,weapons_file):
        self.name = name
        self.kd = self.getKD(player_file)
        self.winp = self.getWinPercentage(player_file)
        self.top_agent = self.getTopAgent(character_file)
        self.headshot_percentage = self.getHeadshotPercentage(player_file)
        self.clutches = self.getClutches(player_file)
        self.first_deaths = self.getFirstDeaths(player_file)
        self.first_kills = self.getFirstBloods(player_file)
        self.knife_kills = self.getKnifeKills(weapons_file)
        self.one_four_nine_damage_done = self.getOneFourNineDamageDone(weapons_file)
        self.rank = self.calculateRank()
        self.archetype = self.assignArchetype()

    def getKD(self,player_file):
        data = openJsonFile(player_file)
        stats = data['stats']
        return stats['kd_ratio']
    
    def getWinPercentage(self,player_file):
            try:
                data = openJsonFile(player_file)
                stats = data['stats']
                wins = stats['matches_won']
                played = stats['matches_played']
                return round((wins/played) * 100)
            except:
                return 50

    def getTopAgent(self,character_file):
        data = openJsonFile(character_file)
        agent_list = data['characters']
        top_agent = agent_list[0]
        top_agent_info = top_agent['character']
        return top_agent_info['name']

    def getHeadshotPercentage(self,player_file):
        data = openJsonFile(player_file)
        stats = data['stats']
        return stats['headshots_percent']

    def getClutches(self,player_file):
        data = openJsonFile(player_file)
        stats = data['stats']
        return stats['clutches']

    def getFirstDeaths(self,player_file):
        data = openJsonFile(player_file)
        stats = data['stats']
        return stats['first_deaths']
    
    def getFirstBloods(self,player_file):
        data = openJsonFile(player_file)
        stats = data['stats']
        return stats['first_bloods']

    def getKnifeKills(self,weapon_file):
        data = openJsonFile(weapon_file)
        weapons_list = data['weapons']

        for i,weapon in enumerate(weapons_list):
            metadata = weapon['metadata']
            weapon_name = metadata['name']
            try:
                if "Melee" in weapon_name:
                    melee_data = weapons_list[i]
                    stats = melee_data['stats']
                    return stats['kills']
            except:
                print("No knife kills :(")
                return 0
        return 0

    def getOneFourNineDamageDone(self,weapon_file):
        data = openJsonFile(weapon_file)
        weapons_list = data['weapons']
        
        for i,weapon in enumerate(weapons_list):
            metadata = weapon['metadata']
            weapon_name = metadata['name']
            try:
                if "Phantom" in weapon_name:
                    phantom_data = weapons_list[i]
                    stats = phantom_data['stats']
                    hits_with_a_kill = stats['kill_conversion']
                    
                    accuracy = stats['accuracy']
                    headshot_percent = accuracy['headshots_percent']
                    head_shots = accuracy['headshots']
                    body_shots = accuracy['bodyshots']
                    leg_shots = accuracy['legshots']
                    
                    total_hits = head_shots + body_shots + leg_shots
                    hits_without_a_kill = 1.0 - hits_with_a_kill
                    head_shots_without_a_kill = (headshot_percent/100) * hits_without_a_kill
                    
                    return round(total_hits * head_shots_without_a_kill)
            except:
                print("No Phantom Kills :(")
                return 0

    def calculateRank(self):
        #Score Assignments
        kd_score = .3
        win_rate_score = .2
        clutch_score = .2
        first_blood_score = .1
        knife_kills = .1
        one_four_nine_score = .1

        #Score Calculations
        base_score = (
            (self.kd * kd_score) + (self.winp * win_rate_score) + (self.clutches * clutch_score) + 
            (self.first_kills * first_blood_score) + (self.one_four_nine_damage_done * one_four_nine_score)
        )/100
        
        for rank, threshold in RANKS.items():
            if base_score >= threshold:
                return rank
        return "Nickel"

    def assignArchetype(self):
        stats = {
            'Clutches' : self.clutches,
            'first_deaths' : self.first_deaths,
            'hs_perc' : self.headshot_percentage,
            'first_kills' : self.first_kills,
            'knife_kills' : self.knife_kills,
            'winp' : self.winp
        }
        archetype_list = []
        for archetype, condition in ARCHETYPES.items():
            if condition(stats):
                archetype_list.append(archetype)
        if not archetype_list:
            archetype_list.append("Basic")
        return archetype_list
    
    def export_to_excel(self, file_name="player_stats.xlsx"):
        player_data = {
            "Name": self.name,
            "KD": self.kd,
            "Win percentage": self.winp,
            "Top Agent": self.top_agent,
            "Headshot Percentage": self.headshot_percentage,
            "Clutches": self.clutches,
            "First Kills": self.first_kills,
            "First Deaths": self.first_deaths,
            "Knife Kills": self.knife_kills,
            "149 Damage Done": self.one_four_nine_damage_done,
            "Rank": self.rank,
            "Archetype": self.archetype,
        }

        # Create dataframe with a single row
        df = pd.DataFrame([player_data])

        if os.path.isfile(file_name):
            # If the file exists, append data to it
            with pd.ExcelWriter(file_name, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, index=False, header=False, startrow=writer.sheets["Sheet1"].max_row)
        else:
            # If the file does not exist, create it with headers
            df.to_excel(file_name, index=False, engine="openpyxl")
        print(f"{self.name}'s stats successfully exported to Excel sheet '{file_name}'.")

class Teamate: #Object for current players team mates, changes each a new game is loaded. Current player also gets a object for this
    def __init__(self,game_file,player_name):
        self.name = player_name
        self.kills = self.getKills(game_file,player_name)
        self.deaths = self.getDeaths(game_file,player_name)
        self.assists = self.getAssists(game_file,player_name)
        self.hs_perc = self.getHSPercentage(game_file,player_name)
        self.team = self.getTeam(game_file,player_name)
        self.agent = self.getAgent(game_file,player_name)
        self.multi_kills = self.getMultiKills(game_file,player_name)

    def getKills(self,game_file,current_player_name):
        data = openJsonFile(game_file)
        match = data['match']
        players = match['players']
        for player in players:
            platform_info = player['platform_info']
            player_name = platform_info['platform_user_nick']
            if player_name in current_player_name:
                stats = player['stats']
                kills = stats['kills']
                return kills
            else:
                continue
    
    def getDeaths(self,game_file,current_player_name):
        data = openJsonFile(game_file)
        match = data['match']
        players = match['players']
        for player in players:
            platform_info = player['platform_info']
            player_name = platform_info['platform_user_nick']
            if player_name in current_player_name:
                stats = player['stats']
                deaths = stats['deaths']
                return deaths
            else:
                continue      

    def getAssists(self,game_file,current_player_name):
        data = openJsonFile(game_file)
        match = data['match']
        players = match['players']
        for player in players:
            platform_info = player['platform_info']
            player_name = platform_info['platform_user_nick']
            if player_name in current_player_name:
                stats = player['stats']
                assists = stats['assists']
                return assists
            else:
                continue      

    def getHSPercentage(self,game_file,current_player_name):
        data = openJsonFile(game_file)
        match = data['match']
        players = match['players']
        for player in players:
            platform_info = player['platform_info']
            player_name = platform_info['platform_user_nick']
            if player_name in current_player_name:
                stats = player['stats']
                accuracy = stats['accuracy']
                hs_perc = accuracy['headshots_percent']
                return hs_perc
            else:
                continue
        
    def getTeam(self,game_file,current_player_name):
            data = openJsonFile(game_file)
            match = data['match']
            players = match['players']
            for player in players:
                platform_info = player['platform_info']
                player_name = platform_info['platform_user_nick']
                if player_name in current_player_name:
                    metadata = player['metadata']
                    team = metadata['team_id']
                    return team
                else:
                    continue
    def getAgent(self,game_file,current_player_name):
            data = openJsonFile(game_file)
            match = data['match']
            players = match['players']
            for player in players:
                platform_info = player['platform_info']
                player_name = platform_info['platform_user_nick']
                if player_name in current_player_name:
                    metadata = player['metadata']
                    character = metadata['character']
                    agent = character['name']
                    return agent
                else:
                    continue
    
    def getMultiKills(self,game_file,current_player_name):
        multi_kills = 0
        data = openJsonFile(game_file)
        match = data['match']
        players = match['players']
        for player in players:
            round_results = player['round_results']
            platform_info = player['platform_info']
            player_name = platform_info['platform_user_nick']
            if player_name in current_player_name:
                for round in round_results:
                    kills = round['kills']
                    if kills >= 3:
                        multi_kills += 1
                return multi_kills
            else:
                continue
        
class Game: #Game specific information
    def __init__(self,game_file):
        self.players = self.getPlayers(game_file)
        self.red_team = self.createRedTeam(game_file)
        self.blue_team = self.createBlueTeam(game_file)
        self.map_name = self.getMapName(game_file)
    
    def getPlayers(self,game_file):
        try:
            players_list = []
            data = openJsonFile(game_file)
            players = data['match']["players"]
            for player in players:
                platform_info = player['platform_info']
                player_name = platform_info['platform_user_nick']
                players_list.append(player_name)
            return players_list
        except Exception as e:
            print(e)
    
    def createRedTeam(self,game_file):
        try:
            red_team = []
            data = openJsonFile(game_file)
            players = data['match']["players"]
            for player in players:
                platform_info = player['platform_info']
                player_name = platform_info['platform_user_nick']
                metadata = player['metadata']
                team = metadata['team_id']
                if "Red" in team:
                    red_team.append(player_name)
            return red_team
        except Exception as e:
            print(e)
    
    def createBlueTeam(self,game_file):
        try:
            blue_team = []
            data = openJsonFile(game_file)
            players = data['match']["players"]
            for player in players:
                platform_info = player['platform_info']
                player_name = platform_info['platform_user_nick']
                metadata = player['metadata']
                team = metadata['team_id']
                if "Blue" in team:
                    blue_team.append(player_name)
            return blue_team
        except Exception as e:
            print(e)

    
    def getMapName(self,game_file):
        try:
            data = openJsonFile(game_file)
            _map = data['match']['map']
            return _map['name']
        except Exception as e:
            print(e)

class Matches: #Class for match history
    def __init__(self,matches_file):
        self.names = self.getNames(matches_file)
        self.current_rank = self.getCurrentRank(matches_file)
        self.agents_played = self.getAgents(matches_file)
        self.gameAPILink = self.getGameID(matches_file)

    def getNames(self,matches_file):
        try:
            match_names = []
            data = openJsonFile(matches_file)
            match_list = data['matches']
            for match in match_list:
                metadata = match['metadata']
                _map = metadata['map']
                name = _map["name"]
                match_names.append(name)
            return match_names
        except Exception as e:
            print(e)
    
    def getAgents(self,matches_file):
        try:
            agent_names = []
            data = openJsonFile(matches_file)
            match_list = data['matches']
            for match in match_list:
                metadata = match['metadata']
                character = metadata['character']
                name = character['name']
                agent_names.append(name)
            return agent_names
        except Exception as e:
            print(e)

    def getCurrentRank(self,matches_file):
        try:
            current_rank = []
            data = openJsonFile(matches_file)
            match_list = data['matches']
            for match in match_list:
                stats = match['stats']
                rank = stats['rank_name']
                current_rank.append(rank)
            return current_rank
        except Exception as e:
            print(e)
    
    def getGameID(self,matches_file):
        try:
            game_id = []
            data = openJsonFile(matches_file)
            match_list = data['matches']
            for match in match_list:
                metadata = match['metadata']
                id = metadata['id']
                game_id.append(id)
            return game_id
        except Exception as e:
            print(e)

class Economy:
    def __init__(self,game_file,red_team,blue_team):
        self.red_team = red_team
        self.red_economy = self.getRedEconomy(game_file,red_team)
        self.blue_team = blue_team
        self.blue_economy = self.getBlueEconomy(game_file,blue_team)

    def getBlueEconomy(self,game_file,blue_team):
        data = openJsonFile(game_file)
        match = data['match']
        players = match['players']

        round_econ = [0] * len(match['rounds'])
        win_econ = [0] * len(match['rounds'])
        kill_econ = [0] * len(match['rounds'])

        for player in players:
            platform_info = player['platform_info']
            player_name = platform_info['platform_user_nick']
            if player_name in blue_team:
                rounds = match['rounds']
                for i,round in enumerate(rounds):
                    winning_team = round['winning_team']
                    if "Blue" in winning_team:
                        win_econ[i] += 3000
                    else:
                        win_econ[i] += 1900


                round_results = player['round_results']
                for i,result in enumerate(round_results):
                    kills = result['kills']
                    kill_bonus = kills * 200
                    kill_econ[i] += kill_bonus
        econ_data = []
        for i,total in enumerate(round_econ):
            total_econ = kill_econ[i]+win_econ[i]
            econ_data.append((i,total_econ))

        print(econ_data)
        return econ_data
    
    def getRedEconomy(self,game_file,red_team):
            data = openJsonFile(game_file)
            match = data['match']
            players = match['players']

            round_econ = [0] * len(match['rounds'])
            win_econ = [0] * len(match['rounds'])
            kill_econ = [0] * len(match['rounds'])

            for player in players:
                platform_info = player['platform_info']
                player_name = platform_info['platform_user_nick']
                if player_name in red_team:
                    rounds = match['rounds']
                    for i,round in enumerate(rounds):
                        winning_team = round['winning_team']
                        if "Red" in winning_team:
                            win_econ[i] += 3000
                        else:
                            win_econ[i] += 1900


                    round_results = player['round_results']
                    for i,result in enumerate(round_results):
                        kills = result['kills']
                        kill_bonus = kills * 200
                        kill_econ[i] += kill_bonus
            econ_data = []
            for i,total in enumerate(round_econ):
                total_econ = kill_econ[i]+win_econ[i]
                econ_data.append((i,total_econ))

            print(econ_data)
            return econ_data
                


    


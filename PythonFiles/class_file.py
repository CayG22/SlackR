from stats_file import *
from utils import openJsonFile
class Player:
    def __init__(self,name,team):
        self.name = name
        self.team = team
        self.kills = 0
        self.money = 0
    
    
    def display_info(self): #Displays player info
        """Displays player's name and team"""
        print(f"Player: {self.name}, Team: {self.team}")

    def check_team_round_outcome(self,game): #Checks whether players team either wins or loses the roudn
        data = openJsonFile(game)

        rounds = data['match']['rounds']
        round_results = []
        for round_data in rounds:
            round_num = round_data['round_num']
            winning_team = round_data['winning_team']
            round_outcome = round_data['round_result_code']

            if self.team == winning_team:
                round_results.append(f"Round {round_num}: Won")
            else:
                round_results.append(f"Round {round_num}: Lost")
        
        return round_results
    
    def check_kills_per_round(self, game): #Checks for players kills per round
        data = openJsonFile(game)
        players = data['match']['players']
        round_kills = {}  # Store kills per round for this player

        for player in players:
            if player['platform_info']['platform_user_nick'] == self.name:
                rounds = player['round_results']
                for round_data in rounds:
                    round_num = round_data['round_num']
                    kills = round_data['kills']
                    round_kills[round_num] = kills  # Store kills for this round

        return round_kills  # Return a dictionary of kills per round
    
    def calculate_money(self, game):
        round_outcomes = self.check_team_round_outcome(game)
        kills_per_round = self.check_kills_per_round(game)  # Returns a dictionary
        total_money = 0
        round_money = []
        win_reward = 3000
        loss_reward_default = 1900  # Default loss reward
        kill_reward = 200  # Reward for each kill

        # Track the last three round outcomes for economy calculation
        recent_losses = []

        for i, outcome in enumerate(round_outcomes):
            # Calculate money based on round outcome
            if "Won" in outcome:
                round_money.append(win_reward)
                total_money += win_reward
                # Reset the recent losses on a win
                recent_losses = []
            else:
                # Determine the loss reward based on recent losses
                recent_losses.append(outcome)
                # Limit the recent losses to the last three rounds
                if len(recent_losses) > 3:
                    recent_losses.pop(0)  # Remove the oldest outcome

                # Calculate the loss reward based on consecutive losses
                if len(recent_losses) == 3 and all("Lost" in x for x in recent_losses):
                    loss_reward = 2900
                elif len(recent_losses) == 2 and all("Lost" in x for x in recent_losses[-2:]):
                    loss_reward = 2400
                else:
                    loss_reward = loss_reward_default

                round_money.append(loss_reward)
                total_money += loss_reward
            
            # Add money for kills in the current round
            round_num = i + 1  # Round numbers start from 1
            kills = kills_per_round.get(round_num, 0)  # Get the number of kills
            total_money += kills * kill_reward  # Add money for kills
            round_money[-1] += kills * kill_reward  # Update the round money list

        self.money = total_money  # Update player's total money

        return round_money, total_money
    
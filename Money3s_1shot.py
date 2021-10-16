team = ''
opp = ''
#if you want to look at playoffs as a whole set team to '0' 
#if you want to look at team as a whole set opp to '0'


##############################################################################

#this pulls all the game files with the team and opponent of interest
#by the end they are stored in a list called team_matchup

#                                                       CHECK YEAR \/
import os
directory = r'C:\Users\maxfi\Desktop\Python\DraftKings\2019-2020_NBA_PbP_Logs\Playoffs'
team_game_files = list()
for filename in os.listdir(directory):
    if filename.find(team) != (-1):
        team_game_files.append((os.path.join(directory, filename)))
    else:
        continue

team_matchup = list()
for opponent in team_game_files:
    if opponent.find(opp) != (-1):
        team_matchup.append(opponent)
    else:
        continue
##############################################################################   


import pandas as pd
team_winnings = []
team_losses = []

for game in team_matchup:
    raw_game = pd.read_csv(game)
    away_score = raw_game.loc[:, "away_score"]  #away team score 
    home_score = raw_game.loc[:, "home_score"]  #home team score
    sum_score = away_score + home_score         #sum of the team scores
    sum_score = sum_score.values                #converts to array
    change_score = [0]*(sum_score.size - 1)     #blank array for change in score

#for loop steps through and takes the difference in score through each index
    for i in range(len(sum_score[1:])):
        change_score[i] = sum_score[i] - sum_score[i-1]
    
    change_score[0] = 0 #something glitchy w/ the first value
    change_score = [j for j in change_score if j != 0] #removes 0's
    change_score = [j for j in change_score if j != 1] #removes 1's

#change score is now a condensed list of 2's and 3's
    bet = 1
    winnings = 0
    losses = 0

#the following embedded loops back test the gambling model:
    #after a 3 bet that the next basket is also a 3
    #if wrong, double the bet that the next basket is a 3
    #if both were wrong, wait until the next 3 is made

    for basket in range(len(change_score[0:-2])):  
        if winnings - losses <= (-100*bet): #stopper at -10 units
            continue
        else:
            if change_score[basket] == 3:
                if change_score[basket + 1] == 3:
                    winnings += (2 * bet)
                else:
                    losses += bet
                    if change_score[basket + 2] == 3:
                        winnings += (4 * bet)
                    else:
                        losses += (2 * bet)
    
    if change_score[-2] == 3:
        if change_score[-1] == 3:
            winnings+= (2 * bet)
        else:
            losses+= bet
    
    
    team_winnings.append(winnings)
    team_losses.append(losses)
##############################################################################


import numpy
Team_winnings = numpy.array(team_winnings)
Team_losses = numpy.array(team_losses)
net_earnings = Team_winnings - Team_losses
Sum_earnings = sum(net_earnings)

print(Sum_earnings)
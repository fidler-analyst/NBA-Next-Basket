team = '0'
opp = '0'
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
counter2s = []

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

#change score is now a condensed array of 2's and 3's


#the following loop determines when 3's occurred 
    counter = 0
    for basket in range(len(change_score[0:-1])):      
        if change_score[basket] == 2:
            if change_score[basket + 1] == 2:
                counter += 1
            elif change_score[basket + 1] == 3:   
                counter2s.append(counter)
                counter = 0
    
##############################################################################

maximum = max(counter2s)
my_bins = range(0, maximum)

import matplotlib.pyplot as plt
#plt.hist(counter2s, bins=my_bins)

counts, bins, bars = plt.hist(counter2s, bins=my_bins)




print(team)
print(len(counter2s))
print(counts)
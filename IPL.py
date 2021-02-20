#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:42:11 2021

@author: imran
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

seasons = matches.groupby('season')

plt.bar(x=seasons.groups.keys(), height=seasons.size())
plt.title('Total played match per season')
plt.show()

stats = {}
#statistics = pd.DataFrame(columns=['year', 'details'])
for name, group in seasons:
    temp = pd.DataFrame()
    temp['teams'] = np.unique(group[['team1','team2']].values)
    lst_won = []
    lst_played = []
    lst_no_result = []
    for team in temp['teams']:
        lst_won.append(group['winner'].value_counts()[team])
        lst_played.append(group['team1'].append(group['team2']).value_counts()[team])
        lst_no_result.append(len(group[((group['team1'] == team) | (group['team2'] == team)) & (group['result'] == 'no result')]))
        #lst_no_result.append(pd.value_counts(group[group['result'].map(lambda x: str(x)=='no result').values.flatten()]))
    temp['played'] = lst_played    
    temp['wins'] = lst_won    
    temp['lost'] = temp['played'] - temp['wins'] - lst_no_result
    temp['no result'] = lst_no_result
    temp = temp.sort_values('wins', ascending=False)
    stats[name] = temp


#Total wins of a team
total_stats = pd.DataFrame()
for year, stat in stats.items():
    total_stats = total_stats.append(stat)

total_stats_grouped = total_stats.groupby('teams').agg({'played': 'sum', 'wins': 'sum'})
total_stats_grouped['Win percentage'] = round(((total_stats_grouped['wins'] / total_stats_grouped['played']) * 100), 2)
Most_successful_team_played_least_70_match = (total_stats_grouped[total_stats_grouped['played'] >= 70]).sort_values(['Win percentage'], ascending=False)

del([total_stats, year, stat, temp, team, seasons, name, lst_won, lst_played, lst_no_result, group])
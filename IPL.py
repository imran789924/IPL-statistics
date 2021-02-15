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
    lst = []
    lst_played = []
    for team in temp['teams']:
        lst.append(group['winner'].value_counts()[team])
        lst_played.append(group['team1'].append(group['team2']).value_counts()[team])
    temp['wins'] = lst
    temp['played'] = lst_played
    temp['lost'] = temp['played'] - temp['wins']
    stats[name] = temp
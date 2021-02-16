#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 11:43:06 2021

@author: imran
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

#player_grouped = deliveries.groupby('batsman')[['batsman_runs', 'match_id']].agg(['sum', 'nunique'])

#player_grouped = deliveries.groupby(['batsman', 'batting_team']).agg({'' })

player_in_teams = (deliveries.groupby(['batsman', 'batting_team'])
                                              .agg({'match_id': 'nunique',
                                                    'batsman_runs': 'sum',
                                                    'over': 'count'})
                                              .reset_index(drop=False)
                                              .rename(columns={'match_id' : 'Played',
                                                               'batsman_runs' : 'Total Runs',
                                                               'batting_team' : 'Team',
                                                               'over' : 'Ball faced'}))
player_in_teams.name = 'Players scored run in each team'


player_stats = (deliveries.groupby(['batsman'])
                                              .agg({'match_id': 'nunique',
                                                    'batsman_runs': 'sum',
                                                    'over' : 'count'
                                                    })
                                              .reset_index(drop=False)
                                              .rename(columns={'match_id' : 'Played',
                                                               'batsman_runs' : 'Total Runs',
                                                               'over' : 'Ball faced'}))

player_stats['Strike Rate'] = round(((player_stats['Total Runs'] / player_stats['Ball faced']) * 100), 1)
#temp = delivery.groupby('batsman')['batsman_runs'].value_counts().reset_index(drop=False)
temp_4 = deliveries[deliveries['batsman_runs'] == 4].groupby('batsman')['batsman_runs'].value_counts()
temp_6 = deliveries[deliveries['batsman_runs'] == 6].groupby('batsman')['batsman_runs'].value_counts()
temp_4 = temp_4.rename('4\'s').reset_index()
temp_4 = temp_4.drop('batsman_runs', axis=1)
temp_6 = temp_6.rename('6\'s').reset_index()
temp_6 = temp_6.drop('batsman_runs', axis=1)

player_stats = player_stats.merge(temp_4, on='batsman', how='left')
player_stats = player_stats.merge(temp_6, on='batsman', how='left')

player_stats.name = 'Most runs in IPL'

player_in_teams.sort_values(['Total Runs', 'Played'], ascending = False, inplace=True)
player_stats.sort_values(['Total Runs', 'Played'], ascending = False, inplace=True)
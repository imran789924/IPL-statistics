#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 23:00:34 2021

@author: imran
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

deliveries.loc[((deliveries['wide_runs'] > 0) & (deliveries['batsman_runs'] != 0)), 'batsman_runs'] = 0
deliveries = deliveries[deliveries['is_super_over'] == 0]


toss_contribution_factor = (matches['toss_winner'] == matches['winner']).value_counts()

batt_fielding = matches[matches['toss_decision']  == 'field']
batting_first_contribution = (batt_fielding['toss_winner'] != batt_fielding['winner']).value_counts()
batt_batting = matches[matches['toss_decision']  == 'bat']
batting_first_contribution_2 = (batt_batting['toss_winner'] == batt_batting['winner']).value_counts()

batting_order_contribution_factor = batting_first_contribution + batting_first_contribution_2
batting_order_contribution_factor.index = ['Win Chasing', 'Win Batting First']

del([batt_fielding, batt_batting, batting_first_contribution, batting_first_contribution_2])

group = deliveries.groupby(['match_id', 'batting_team'])

open_part = []
runs_6_over = []
wickets_6_over = []
for match, inning in group:
    temp = 0
    for j in range(len(inning)):
        if(pd.isnull(inning['player_dismissed'].iloc[j])):
            temp = temp + inning['batsman_runs'].iloc[j]
        else:
            break
    a = list(match)
    a.extend([temp])
    open_part.append(a)
    
    temp = 0
    for j in range(30):
        try:
            temp = temp + inning['total_runs'].iloc[j]
        except:
            temp = temp + 0
    a = list(match)
    a.extend([temp])
    runs_6_over.append(a)
    
    temp = 0
    for j in range(30):
        try:
            if(pd.isnull(inning['player_dismissed'].iloc[j])):
                temp = temp + 0
            else:
                temp = temp + 1
        except:
            temp = temp + 0
    print(temp)
    a = list(match)
    a.extend([temp])
    wickets_6_over.append((a))

opening_partnerships = pd.DataFrame(open_part)
runs_first_6_over = pd.DataFrame(runs_6_over)
wickets_first_6_over = pd.DataFrame(wickets_6_over)

del([a, open_part, j, inning, temp, runs_6_over, wickets_6_over])

#opening_partnerships_30_more = [[j for j in x] for x in opening_partnerships]

opening_partnerships_50_more = opening_partnerships[opening_partnerships[2] >= 50]
opening_partnerships_50_more.columns = ['id', 'team', 'partnership'] 

runs_first_6_over_more = runs_first_6_over[runs_first_6_over[2] >= 50]
runs_first_6_over_more.columns = ['id', 'team', 'Runs scored']

wicket_first_6_over_more = wickets_first_6_over[wickets_first_6_over[2] >= 3]
wicket_first_6_over_more.columns = ['id', 'team', 'wickets']


Opening_partnership_winning_factor = opening_partnerships_50_more.merge(matches[['id','winner']], on='id', how='left')
Opening_partnership_winning_factor = Opening_partnership_winning_factor.sort_values(['id','partnership']).drop_duplicates('id', keep='last')
Opening_partnership_winning_factor = (Opening_partnership_winning_factor['team'] == Opening_partnership_winning_factor['winner']).value_counts()
Opening_partnership_winning_factor.index = ['Matches Won', 'Matches Lost']


first_6_over_run_winning_factor = runs_first_6_over_more.merge(matches[['id','winner']], on='id', how='left')
first_6_over_run_winning_factor = first_6_over_run_winning_factor.sort_values(['id','Runs scored']).drop_duplicates('id', keep='last')
first_6_over_run_winning_factor = (first_6_over_run_winning_factor['team'] == first_6_over_run_winning_factor['winner']).value_counts()
first_6_over_run_winning_factor.index = ['Matches Won', 'Matches Lost']


first_6_over_wicket_winning_factor = wicket_first_6_over_more.merge(matches[['id','winner']], on='id', how='left')
first_6_over_wicket_winning_factor = first_6_over_wicket_winning_factor.sort_values(['id','wickets']).drop_duplicates('id', keep='last')
first_6_over_wicket_winning_factor = (first_6_over_wicket_winning_factor['team'] == first_6_over_wicket_winning_factor['winner']).value_counts()
first_6_over_wicket_winning_factor.index = ['Matches Won', 'Matches Lost']

del(opening_partnerships_50_more, runs_first_6_over_more, wicket_first_6_over_more)



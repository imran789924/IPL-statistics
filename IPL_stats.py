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

player_in_teams = (deliveries[deliveries['wide_runs'] == 0].groupby(['batsman', 'batting_team'])
                                              .agg({'match_id': 'nunique',
                                                    'batsman_runs': 'sum',
                                                    'over': 'count'})
                                              .reset_index(drop=False)
                                              .rename(columns={'match_id' : 'Played',
                                                               'batsman_runs' : 'Total Runs',
                                                               'batting_team' : 'Team',
                                                               'over' : 'Ball faced'}))
player_in_teams.name = 'Batman scored run in each team'


batsman_stats = (deliveries[deliveries['wide_runs'] == 0].groupby(['batsman'])
                                              .agg({'match_id': 'nunique',
                                                    'batsman_runs': 'sum',
                                                    'over' : 'count'
                                                    })
                                              .reset_index(drop=False)
                                              .rename(columns={'match_id' : 'Played',
                                                               'batsman_runs' : 'Total Runs',
                                                               'over' : 'Ball faced'}))

batsman_stats['Strike Rate'] = (round(((batsman_stats['Total Runs'] 
                                        / batsman_stats['Ball faced']) * 100), 1))
#temp = delivery.groupby('batsman')['batsman_runs'].value_counts().reset_index(drop=False)
temp_4 = deliveries[deliveries['batsman_runs'] == 4].groupby('batsman')['batsman_runs'].value_counts()
temp_6 = deliveries[deliveries['batsman_runs'] == 6].groupby('batsman')['batsman_runs'].value_counts()
temp_4 = temp_4.rename('4\'s').reset_index()
temp_4 = temp_4.drop('batsman_runs', axis=1)
temp_6 = temp_6.rename('6\'s').reset_index()
temp_6 = temp_6.drop('batsman_runs', axis=1)

batsman_stats = batsman_stats.merge(temp_4, on='batsman', how='left')
batsman_stats = batsman_stats.merge(temp_6, on='batsman', how='left')

del([temp_4, temp_6])

batsman_stats.name = 'Most runs in IPL'

player_in_teams.sort_values(['Total Runs', 'Played'], ascending = False, inplace=True)
batsman_stats.sort_values(['Total Runs', 'Played'], ascending = False, inplace=True)




#######################################################################################
#Bowler


deliveries['consided runs'] = deliveries.iloc[:, [10,13,15]].sum(axis=1)

bowler_in_teams = (deliveries[~((deliveries['wide_runs'] > 0) | (deliveries['noball_runs'] > 0))].groupby(['bowler', 'bowling_team'])
                                              .agg({'match_id': 'nunique',
                                                    'consided runs': 'sum',
                                                    'over': 'count'})
                                              .reset_index(drop=False)
                                              .rename(columns={'match_id' : 'Played',
                                                               'consided runs' : 'Runs Given',
                                                               'bowling_team' : 'Team',
                                                               'over' : 'Balls'}))
bowler_in_teams.name = 'Bowlers statistics in each team'


bowler_stats = (deliveries[~((deliveries['wide_runs'] > 0) | (deliveries['noball_runs'] > 0))].groupby(['bowler'])
                                              .agg({'match_id': 'nunique',
                                                    'consided runs': 'sum',
                                                    'over' : 'count'
                                                    })
                                              .reset_index(drop=False)
                                              .rename(columns={'match_id' : 'Played',
                                                               'consided runs' : 'Runs Given',
                                                               'over' : 'Balls'}))


bowler_stats['Economy'] = round((bowler_stats['Runs Given'] / (bowler_stats['Balls'] / 6)), 1)
#temp = delivery.groupby('batsman')['batsman_runs'].value_counts().reset_index(drop=False)
temp_wicket_filters = (pd.notnull(deliveries['dismissal_kind']) 
                           & (deliveries['dismissal_kind'] != 'retired hurt') 
                           & (deliveries['dismissal_kind'] != 'run out') 
                           & (deliveries['dismissal_kind'] != 'obstructing the field'))

temp_wickets = (deliveries[temp_wicket_filters]
                           .groupby('bowler')['dismissal_kind'].count()
                           .reset_index(drop=False)
                           .rename(columns={'dismissal_kind' : 'Wickets'}))

bowler_stats = bowler_stats.merge(temp_wickets, on='bowler', how='left')

bowler_wickets_each_match = deliveries[temp_wicket_filters].groupby(['match_id', 'bowler'])['dismissal_kind'].count().reset_index(drop=False)





temp = bowler_wickets_each_match.groupby('bowler').agg({'dismissal_kind':'idxmax'}).reset_index(drop=False)
temp_best_fig_wickets = bowler_wickets_each_match.iloc[temp.iloc[:,1]]
del(temp)
#temp_best_fig_wickets = bowler_wickets_each_match.merge(temp, on=['bowler', 'dismissal_kind'], how='right')



#temp_best_fig_wickets = bowler_wickets_each_match[temp.isin(bowler_wickets_each_match['dismissal_kind'])]

temp_best_fig_runs_raw = deliveries.merge(temp_best_fig_wickets, on=['match_id','bowler'], how='right')

temp_best_fig = temp_best_fig_runs_raw[temp_best_fig_runs_raw['is_super_over'] == 0].groupby(['bowler', 'match_id'])['consided runs'].sum().reset_index(drop=False)

temp_best_fig_final = temp_best_fig.merge(temp_best_fig_wickets, on=['match_id', 'bowler'], how='inner')

temp_best_fig_final = temp_best_fig_final.astype(str)
temp_best_fig_final['Best Figure'] = temp_best_fig_final[['consided runs', 'dismissal_kind']].agg('/'.join, axis=1)
#c = bowler_stats[~bowler_stats.bowler.isin(temp_best_fig_wickets.reset_index(drop=False)['bowler'])]['bowler']
temp_best_fig_final.drop(columns=['consided runs','dismissal_kind'], axis=1, inplace=True)
bowler_stats = bowler_stats.merge(temp_best_fig_final, on=['bowler'], how='inner')
bowler_stats.drop('match_id', axis=1, inplace=True)


bowler_stats.sort_values(['Wickets', 'Played'], ascending = False, inplace=True)



'''
temp_4 = deliveries[deliveries['dismissal_kind'] != 4].groupby('batsman')['batsman_runs'].value_counts()
temp_6 = deliveries[deliveries['batsman_runs'] == 6].groupby('batsman')['batsman_runs'].value_counts()
temp_4 = temp_4.rename('4\'s').reset_index()
temp_4 = temp_4.drop('batsman_runs', axis=1)
temp_6 = temp_6.rename('6\'s').reset_index()
temp_6 = temp_6.drop('batsman_runs', axis=1)


bowler_stats = batsman_stats.merge(temp_4, on='batsman', how='left')
bowler_stats = batsman_stats.merge(temp_6, on='batsman', how='left')

bowler_stats.name = 'Most runs in IPL'

bowler_in_teams.sort_values(['Total Runs', 'Played'], ascending = False, inplace=True)
bowler_stats.sort_values(['Total Runs', 'Played'], ascending = False, inplace=True)
'''

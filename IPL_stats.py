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

deliveries.loc[((deliveries['wide_runs'] > 0) & (deliveries['batsman_runs'] != 0)), 'batsman_runs'] = 0

#player_grouped = deliveries.groupby('batsman')[['batsman_runs', 'match_id']].agg(['sum', 'nunique'])

#player_grouped = deliveries.groupby(['batsman', 'batting_team']).agg({'' })

batsman_in_teams = (deliveries[(deliveries['wide_runs'] == 0) | (deliveries['is_super_over'] == 0)].groupby(['batsman', 'batting_team'])
                                              .agg({'match_id': 'nunique',
                                                    'batsman_runs': 'sum',
                                                    'over': 'count'})
                                              .reset_index(drop=False)
                                              .rename(columns={'match_id' : 'Innings',
                                                               'batsman_runs' : 'Total Runs',
                                                               'batting_team' : 'Team',
                                                               'over' : 'Ball faced'}))
batsman_in_teams.name = 'Batman scored run in each team'


batsman_stats = (deliveries[(deliveries['wide_runs'] == 0) & (deliveries['is_super_over'] == 0)].groupby(['batsman'])
                                              .agg({'match_id': 'nunique',
                                                    'batsman_runs': 'sum',
                                                    'over' : 'count'
                                                    })
                                              .reset_index(drop=False)
                                              .rename(columns={'match_id' : 'Innings',
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




batsman_run_each_match = deliveries[(deliveries['wide_runs'] == 0) & (deliveries['is_super_over'] == 0)].groupby(['match_id','batsman']).agg({'batsman_runs':'sum'}).reset_index(drop=False)
batsman_highest_score = batsman_run_each_match.groupby('batsman').agg({'batsman_runs':'max'}).reset_index(drop=False).rename(columns={'batsman_runs': 'Highest score'})
batsman_50 = batsman_run_each_match[(batsman_run_each_match['batsman_runs'] >=50) & (batsman_run_each_match['batsman_runs'] < 100)].groupby('batsman').agg({'batsman_runs': 'count'}).reset_index(drop=False).rename(columns={'batsman_runs': '50\'s'})
batsman_100 = batsman_run_each_match[(batsman_run_each_match['batsman_runs'] >=100)].groupby('batsman').agg({'batsman_runs': 'count'}).reset_index(drop=False).rename(columns={'batsman_runs': '100\'s'})

batsman_stats = batsman_stats.merge(batsman_highest_score, on='batsman', how='left')
batsman_stats = batsman_stats.merge(batsman_50, on='batsman', how='left')
batsman_stats = batsman_stats.merge(batsman_100, on='batsman', how='left')



batsman_no_of_dismissals = deliveries[(deliveries['dismissal_kind'] != 'retired hurt') & deliveries['is_super_over'] == 0]['player_dismissed'].value_counts().reset_index(drop=False)
batsman_no_of_dismissals.columns = ['batsman', 'Total dismissals']

batsman_runs_individual = batsman_stats[['batsman', 'Total Runs']].reset_index(drop=False)
batsman_average = batsman_runs_individual.merge(batsman_no_of_dismissals, on='batsman', how='left')

batsman_stats['Average'] = round((batsman_average['Total Runs'] / batsman_average['Total dismissals']), 2)


batsman_stats.fillna(0, inplace=True)


col = ['batsman', 'Innings', 'Total Runs', 'Ball faced', 'Average', 'Highest score', 'Strike Rate', '50\'s', '100\'s', '4\'s', '6\'s']
batsman_stats = batsman_stats[col]

batsman_in_teams.sort_values(['Total Runs', 'Innings'], ascending = False, inplace=True)
batsman_stats.sort_values(['Total Runs', 'Innings'], ascending = False, inplace=True)





#######################################################################################
#Bowler


deliveries['Conceded Runs'] = deliveries[deliveries['is_super_over'] == 0].iloc[:, [10,13,15]].sum(axis=1)

bowler_in_teams = (deliveries[~((deliveries['wide_runs'] > 0) | (deliveries['noball_runs'] > 0))].groupby(['bowler', 'bowling_team'])
                                              .agg({'match_id': 'nunique',
                                                    'Conceded Runs': 'sum',
                                                    'over': 'count'})
                                              .reset_index(drop=False)
                                              .rename(columns={'match_id' : 'Innings',
                                                               'Conceded Runs' : 'Runs Given',
                                                               'bowling_team' : 'Team',
                                                               'over' : 'Balls'}))
bowler_in_teams.name = 'Bowlers statistics in each team'


bowler_stats = (deliveries[~((deliveries['wide_runs'] > 0) | (deliveries['noball_runs'] > 0))].groupby(['bowler'])
                                              .agg({'match_id': 'nunique',
                                                    #'Conceded Runs': 'sum',
                                                    'over' : 'count'
                                                    })
                                              .reset_index(drop=False)
                                              .rename(columns={'match_id' : 'Innings',
                                                               #'Conceded Runs' : 'Runs Given',
                                                               'over' : 'Balls'}))

temp_runs_bowler = deliveries[deliveries['is_super_over'] == 0].groupby('bowler')['Conceded Runs'].sum()

bowler_stats = bowler_stats.merge(temp_runs_bowler, on='bowler', how='inner')
del(temp_runs_bowler)

bowler_stats['Economy'] = round((bowler_stats['Conceded Runs'] / (bowler_stats['Balls'] / 6)), 1)
#temp = delivery.groupby('batsman')['batsman_runs'].value_counts().reset_index(drop=False)
temp_wicket_filters = (pd.notnull(deliveries['dismissal_kind']) 
                           & (deliveries['dismissal_kind'] != 'retired hurt') 
                           & (deliveries['dismissal_kind'] != 'run out') 
                           & (deliveries['dismissal_kind'] != 'obstructing the field')
                           & (deliveries['is_super_over'] == 0))

temp_wickets = (deliveries[temp_wicket_filters]
                           .groupby('bowler')['dismissal_kind'].count()
                           .reset_index(drop=False)
                           .rename(columns={'dismissal_kind' : 'Wickets'}))

bowler_stats = bowler_stats.merge(temp_wickets, on='bowler', how='left')

bowler_wickets_each_match = deliveries[temp_wicket_filters].groupby(['match_id', 'bowler'])['dismissal_kind'].count().reset_index(drop=False)
#bowler_wickets_each_match_test = deliveries[temp_wicket_filters].groupby(['match_id', 'bowler']).agg({'dismissal_kind' : 'count', 'Conceded Runs' : 'sum'}).reset_index(drop=False)

#newline
bowler_runs_each_match = deliveries[deliveries['is_super_over'] == 0].groupby(['match_id', 'bowler']).agg({'Conceded Runs' : 'sum'}).reset_index(drop=False)
bowler_wickets_each_match = bowler_wickets_each_match.merge(bowler_runs_each_match, on=['match_id', 'bowler'], how='left')


#temp = bowler_wickets_each_match.groupby('bowler').agg({'dismissal_kind':'idxmax'}).reset_index(drop=False)
#new line 2
temp = bowler_wickets_each_match.sort_values(['bowler', 'dismissal_kind', 'Conceded Runs'], ascending=[True, False, True])

#temp = bowler_wickets_each_match.groupby('bowler', as_index=True).agg({'dismissal_kind' : 'max', 'Conceded Runs': 'min'}).reset_index(drop=False)

#new line 2
temp1 = temp.groupby('bowler').agg({'dismissal_kind' : 'idxmax'}).reset_index(drop=False)

temp = temp.reset_index(drop=False)

temp2 = temp.iloc[temp1.iloc[:,1]]
temp2 = temp.merge(temp1, left_on = 'index', right_on='dismissal_kind')
temp2.drop(['index', 'match_id', 'bowler_y', 'dismissal_kind_y'], axis=1, inplace=True)
#temp1 = bowler_wickets_each_match.groupby(['match_id', 'bowler']).agg({'Conceded Runs': 'sum'}).reset_index(drop=False)
temp2.columns = ['bowler', 'dismissal_kind', 'Conceded Runs']



#temp_best_fig_wickets = bowler_wickets_each_match.iloc[temp.iloc[:,1]]
temp_best_fig_final = bowler_wickets_each_match.merge(temp2, on=['bowler', 'dismissal_kind', 'Conceded Runs'], how='right')
del(temp)
#temp_best_fig_wickets = bowler_wickets_each_match.merge(temp, on=['bowler', 'dismissal_kind'], how='right')
#temp_best_fig_wickets = bowler_wickets_each_match[temp.isin(bowler_wickets_each_match['dismissal_kind'])]

#temp_best_fig_runs_raw = deliveries.merge(temp_best_fig_wickets, on=['match_id','bowler'], how='right')
#temp_best_fig = temp_best_fig_runs_raw[temp_best_fig_runs_raw['is_super_over'] == 0].groupby(['bowler', 'match_id'])['Conceded Runs'].sum().reset_index(drop=False)

#temp_best_fig_final = temp_best_fig_final.merge(temp_best_fig_wickets, on=['match_id', 'bowler'], how='inner')


temp_best_fig_final = temp_best_fig_final.astype(str)
temp_best_fig_final['Best Figure'] = temp_best_fig_final[['Conceded Runs', 'dismissal_kind']].agg('/'.join, axis=1)
#c = bowler_stats[~bowler_stats.bowler.isin(temp_best_fig_wickets.reset_index(drop=False)['bowler'])]['bowler']
temp_best_fig_final.drop(columns=['Conceded Runs','dismissal_kind'], axis=1, inplace=True)
bowler_stats = bowler_stats.merge(temp_best_fig_final, on=['bowler'], how='inner')
bowler_stats.drop('match_id', axis=1, inplace=True)




bowler_stats['Best Figure'] = bowler_stats['Best Figure'].str.replace('\.\d+', '')

temp_3 = bowler_wickets_each_match[(bowler_wickets_each_match['dismissal_kind'] >= 3) & (bowler_wickets_each_match['dismissal_kind'] < 5)].groupby('bowler').agg({'dismissal_kind': 'count'}).reset_index(drop=False).rename(columns={'dismissal_kind' : '3 wickets'})
temp_5 = bowler_wickets_each_match[bowler_wickets_each_match['dismissal_kind'] >= 5].groupby('bowler').agg({'dismissal_kind': 'count'}).reset_index(drop=False).rename(columns={'dismissal_kind' : '5 wickets'})

bowler_stats = bowler_stats.merge(temp_3, on='bowler', how='left')
bowler_stats = bowler_stats.merge(temp_5, on='bowler', how='left')

bowler_stats['Average'] = bowler_stats['Conceded Runs'] / bowler_stats['Wickets']

cols = ['bowler', 'Innings', 'Balls', 'Conceded Runs', 'Wickets', 'Best Figure', 'Average', 'Economy', '3 wickets', '5 wickets']
bowler_stats = bowler_stats[cols]


bowler_stats.fillna(0, inplace=True)

bowler_stats.sort_values(['Wickets', 'Innings'], ascending = False, inplace=True)

del([temp1, temp2, temp_wickets, temp_wicket_filters, temp_best_fig_final, temp_3, temp_5, cols, col, bowler_runs_each_match, batsman_no_of_dismissals, batsman_run_each_match, batsman_runs_individual, batsman_highest_score, batsman_100, batsman_50])

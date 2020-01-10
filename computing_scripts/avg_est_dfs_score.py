import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

# scrapes and saves average player stats when imported.
from scraping_scripts.player_per_game_scrape import player_per_game_std

def avg_dfs_score():
    
    # read in data that was scraped via import statment
    df = pd.read_csv('scraped_data\player_per_game_std_2020.csv')

    # reference for stats and dfs scoring values
    # TODO merge two dicts into one by using the dfs_score_key values as keys
    dfs_point_ref = {'Point': 1.0,
                    'Made 3pt': 0.5,
                    'Rebound': 1.25,
                    'Assist': 1.5,
                    'Steal': 2.0,
                    'Block': 2.0,
                    'Turnover': -0.5}
                    # Double-double': 1.5,    # future feature
                    # 'Triple-double': 3.0    # future feature

    dfs_score_key = {'Point': 'PTS',
                    'Made 3pt': '3P',
                    'Rebound': 'TRB',
                    'Assist': 'AST',
                    'Steal': 'STL',
                    'Block': 'BLK',
                    'Turnover': 'TOV'}
                    # 'Double-double': 'DD%',  # future feature
                    # 'Triple-double': 'TD%'   # future feature

    # converting stats to dfs scoring total per stat
    for stat in dfs_score_key.keys():
        df[dfs_score_key[stat]] = df[dfs_score_key[stat]] * dfs_point_ref[stat]

    # creating average daily fantasy score total per player
    df['ADFS'] = df['PTS'] + df['3P'] + df['TRB'] + df['AST'] + df['STL'] + df['BLK'] + df['TOV']

    # sorting for top ADFS scoring total
    df.sort_values(by='ADFS', ascending=False)

    # printing top 10 ADFS
    print(df[['Player', 'PTS', '3P', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'ADFS']].head(10))
    
    # writing data
    df.to_csv(r'computed_data\avg_dfs_score_exclude_dubs.csv')

    return(df)

# calling function to apply computations 
# and write to csv for storage.
# set to variable for reveiwing data in console.
avg_dfs_score()
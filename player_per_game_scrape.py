import pandas as pd
from bs4 import BeautifulSoup
import requests
import pickle
import numpy as np

def player_per_game_std(year='2020'):
    """
    Returns a dataframe of per game stats by player.
    This is for standard stats, use player_per_game_adv() for
    advanced stats.
    """
    #  getting page content
    source = requests.get('https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'.format(str(year)))
    soup = BeautifulSoup(source.content, 'html.parser')

    #  retrieving the table
    tables = soup.find('table', {'id': 'per_game_stats'})

    # extracting column names
    table_header = soup.find('thead')
    columns = []
    for th in table_header.findAll('th'):
        key = th.get_text()
        columns.append(key)
        headers = columns[1:]

    # extracting datapoints from table body
    table_body = soup.find('tbody')
    data_rows = []
    for tr in table_body.findAll('td'):
        key = tr.get_text()
        data_rows.append(key)

    #  chunking table data, making dataframe, saving to csv.
    row_chunks = [data_rows[x:x+29] for x in np.arange(0, len(data_rows), 29)]
    data = pd.DataFrame(row_chunks, columns=headers)
    data.to_csv('player_per_game_std_{}.csv'.format(str(year)))
    return data


def player_per_game_adv(year='2020'):
    """
    Returns a dataframe of per game stats by player.
    This is for advanced stats, use player_per_game_std() for
    standard stats.
    """
    #  getting page content
    source = requests.get('https://www.basketball-reference.com/leagues/NBA_{}_advanced.html'.format(str(year)))
    soup = BeautifulSoup(source.content, 'html.parser')

    #  retrieving the table
    tables = soup.find('table', {'id': 'advanced_stats'})

    # extracting column names
    table_header = soup.find('thead')
    columns = []
    for th in table_header.findAll('th'):
        key = th.get_text()
        columns.append(key)
        headers = columns[1:]

    # extracting datapoints from table body
    table_body = soup.find('tbody')
    data_rows = []
    for tr in table_body.findAll('td'):
        key = tr.get_text()
        data_rows.append(key)

    #  chunking table data, making dataframe, saving to csv.
    row_chunks = [data_rows[x:x+28] for x in np.arange(0, len(data_rows), 28)]
    data = pd.DataFrame(row_chunks, columns=headers)
    data.drop('\xa0', axis=1)
    data.to_csv('player_per_game_adv_{}.csv'.format(str(year)))
    return data

# calling functions to save to csv, 
# set to variable for saving df.
player_per_game_adv()
player_per_game_std()
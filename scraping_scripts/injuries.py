import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
import datetime as dt 


def get_injury_list():
    source = requests.get('https://www.basketball-reference.com/friv/injuries.fcgi')
    soup = BeautifulSoup(source.content, 'html.parser')

    table = soup.find('table', {'id': 'injuries'})

    table_header = table.find('thead')
    columns = []
    for th in table_header.findAll('th'):
        key = th.get_text()
        columns.append(key)
            
    # getting table body and finding all table data
    table_body = table.find('tbody')
    data_rows = []
    for tr in table_body.findAll('td'):
        key = tr.get_text()
        data_rows.append(key)
        
    # player names stored in th not td like other
    player_col = []
    for th in table_body.findAll('th'):
        key = th.get_text()
        player_col.append(key)
        
    row_chunks = [data_rows[x:x+3] for x in np.arange(0, len(data_rows), 3)]
    complete_rows = [[x] + y for x, y in zip(player_col, row_chunks)]
    data = pd.DataFrame(complete_rows, columns=columns)
    data.to_csv('scraped_data/injuries.csv')

    return data

get_injury_list()

    
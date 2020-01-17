import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
import datetime as dt 
import player_avgs as plyravg
    
    
def get_today_salaries():
    source = requests.get('https://www.fantasypros.com/daily-fantasy/nba/draftkings-salary-changes.php')
    soup = BeautifulSoup(source.content, 'html.parser')

    # getting table headers
    table = soup.find('table', {'id': 'data-table'})
    table_header = table.find('thead')

    columns = []
    for th in table_header.findAll('th'):
        key = th.get_text()
        columns.append(key)
        
    # getting table data (in seperate table)
    table_body = table.find('tbody')
    data_rows = []
    for tr in table_body.findAll('td'):
        key = tr.get_text()
        data_rows.append(key)

    row_chunks = [data_rows[x:x+7] for x in np.arange(0, len(data_rows), 7)]
    data = pd.DataFrame(row_chunks, columns=columns)

    now = dt.datetime.now()
    data.to_csv(f'scraped_data\salaries_{now.month}-{now.day}-{now.year}.csv')
    
    return data

get_today_salaries()

# add in function for appending the estimated fantasy avgs for each player

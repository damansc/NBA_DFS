import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
import os


def pull_schedule_full(year='2020'):
    """
    Pulls the schedule for the specified year.
    Data includes score and also hrefs contain
    a link to the box scores for scraping.
    """

    # months from bball reference listed
    months = ['october', 'november', 'december', 'january', 'february', 'march', 'april']
    # list to hold each months schedule for later concatenation
    month_container = []
    
    for month in months:

        # getting 
        source = requests.get(f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html')
        soup = BeautifulSoup(source.content, 'html.parser')
        table = soup.find('table', {'id': 'schedule'})
        table_header = soup.find('thead')
        
        columns = []
        for th in table_header.findAll('th'):
            key = th.get_text()
            columns.append(key)
            # not including dates in headers since will add later
            headers = columns[1:]
        headers[5:7] = ['Box_Score', 'OT?']

        # extracting datapoints from table body
        table_body = soup.find('tbody')
        data_rows = []
        for tr in table_body.findAll('td'):
            key = tr.get_text()
            data_rows.append(key)

        dates_col = soup.findAll('th', {'data-stat': 'date_game'})
        dates = []
        for x in dates_col:
            dates.append(x.get_text())

        row_chunks = [data_rows[x:x+9] for x in np.arange(0, len(data_rows), 9)]
        data = pd.DataFrame(row_chunks, columns=headers)
        data.insert(0, 'Dates', dates[1:])
        month_container.append(data)
    master = pd.concat(month_container, axis=0)
    master.to_csv(f'scraped_data\schedule_{year}.csv')
    return pd.concat(month_container, axis=0)

        
if __name__ == '__main__':
    print(pull_schedule_full())
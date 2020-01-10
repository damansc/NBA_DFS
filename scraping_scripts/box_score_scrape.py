import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
import os

def get_boxscore_links(year='2020'):

    """
    retrieves all links to every single available box score.
    It seems that bball reference lags behind a bit.
    I ran today (1/6/20) and only through 1/4/20 is up.
    """

    months = ['october', 'november', 'december', 'january', 'february', 'march', 'april']
    root = 'https://www.basketball-reference.com'
    boxscore_links = []
    for month in months:
        source = requests.get(f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html')
        soup = BeautifulSoup(source.content, 'html.parser')
        a_soup = soup.findAll('a')
        a_tags = []

        for a in a_soup:
            if (a.get('href')[0:4] == '/box') & (len(a.get('href')) == 28):
                a_tags.append(a.get('href'))

        for x in a_tags:
            boxscore_links.append(root + x)

    return boxscore_links

test = get_boxscore_links()
source = requests.get(test[1])
page = BeautifulSoup(source.content, 'html.parser')

# getting each table, thead, and tbody
tables = page.findAll('table')
theads = page.findAll('thead')
tbodys = page.findAll('tbody')

# getting each table head
table_body = page.find('tbody')
data_rows = []
for tr in table_body.findAll('td'):
    key = tr.get_text()
    data_rows.append(key)



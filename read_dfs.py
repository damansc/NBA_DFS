import pandas as pd
import os

data_file = os.listdir('../data')
read_str = 'data/{}'.format(data_file)
df = pd.read_csv('data/{}'.format(data_file[0]))

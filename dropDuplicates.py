#!/usr/bin/python3

import pandas as pd


csv_file_name = 'block 3.csv'

df = pd.read_csv(csv_file_name)
df = df.sort_values('obs_time', ascending=True)
df = df.reset_index(drop=True)

# print('Original DF')
# print(df)

df_new = df.drop_duplicates(subset='obs_time', inplace=True)
df_new = df.sort_values('obs_time', ascending=True)

# print('DF dropped duplicates')
# print(df_new)

df_new.to_csv('block 3 dropped.csv', index=False)

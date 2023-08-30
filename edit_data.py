import os
import pandas as pd

input = './crawling_data/webtoon_data.csv'

output = './crawling_data/webtoon_data_final.csv'

df = pd.read_csv(input)
df = df.drop_duplicates(subset=['story'], keep='first')
df.to_csv(output, index=False, encoding='utf-8-sig')

print("Finished")
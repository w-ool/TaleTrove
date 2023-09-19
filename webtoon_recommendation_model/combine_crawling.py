import os
import pandas as pd

input = './crawling_data/'

output = './crawling_data/webtoon_data.csv'

csv_files = [f for f in os.listdir(input) if f.endswith('.csv')]

# csv파일들 읽어와서 하나의 리스트에 저장
data_frames = []
for csv_file in csv_files:
    csv_path = os.path.join(input, csv_file)
    df = pd.read_csv(csv_path)
    data_frames.append(df)

# dataframe 합치기
merged_df = pd.concat(data_frames, ignore_index=True)
# id열 삭제
merged_df = merged_df.drop('id', axis=1)
# 중복 삭제
merged_df = merged_df.drop_duplicates(subset=['title'], keep='first')
# 장르에서 #제거
merged_df['genre'] = merged_df['genre'].str.replace(' ', '')
merged_df['genre'] = merged_df['genre'].str.replace('#', ' ')
merged_df['genre'] = merged_df['genre'].str.lstrip(' ')

merged_df.to_csv(output, index=False, encoding='utf-8-sig')

print("Finished")
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from tqdm import tqdm
import numpy as np
import json

with open('./vector_data/webtoon_vectors_nospace.json', 'r') as json_file:
    data = json.load(json_file)
similarity_list = []
title_list = []
db_vector_list = []
dict = {}

# 제목 받기
user_input = input('제목을 입력해주세요: ')
user_input = user_input.replace(' ', '')

# json에서 각 작품 불러오기
for title in tqdm(data):
    # 각 작품별 백터 추출 
    db_vector = data[title]

    # dict 생성을 위해 vector, title 리스트에 정보 추가
    title_list.append(title)
    db_vector_list.append(db_vector)

# similarity 비교 시작

# 작품에 대한 vector값이 이미 존재하는 경우
if user_input in title_list:
    input_vector = data[user_input]
    
    # 두 백터값 비교후 젤 유사한 값 찾아오기
    for vector, title in zip(db_vector_list, title_list):
        similarity = util.cos_sim(input_vector, vector)
        similarity_list.append(similarity)

        dict[similarity] = title

# vector값이 존재하지 않는 경우
else:
    # 스토리 요약을 받아 vector값 추출
    summary_input = input('스토리 요약을 입력해주세요: ')
    model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
    input_vector = model.encode(summary_input)

    # 두 백터값 비교후 젤 유사한 값 찾아오기
    for vector, title in zip(db_vector_list, title_list):
        similarity = util.cos_sim(input_vector, vector)
        similarity_list.append(similarity)

        dict[similarity] = title

# 유사도 리스트 높은순으로 정렬
similarity_list.sort(reverse=True)

# input이 db에 있어서 100%유사한 경우 제외
if user_input != dict[similarity_list[0]]:
    # top 5개 유사도를 지닌 작품 불러오기
    for i in range(5):
        similarity = similarity_list[i]
        title_sorted = dict[similarity]

        print(f'작품명: {title_sorted}, 유사도: {similarity}')
else:
    # top 5개 유사도를 지닌 작품 불러오기
    for i in range(1,6):
        similarity = similarity_list[i]
        title_sorted = dict[similarity]

        print(f'작품명: {title_sorted}, 유사도: {similarity}')
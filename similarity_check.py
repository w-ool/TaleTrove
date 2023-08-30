from sentence_transformers import SentenceTransformer, util
import pandas as pd
from tqdm import tqdm
import numpy as np

webtoon_df = pd.read_csv('./naver_unfinished_vector.csv')
vectors = webtoon_df['vector']
count = 0
vector_list = []

for vector in vectors:
    vector_list.append(float(vector))

vector_array = np.array(vector_list)

while count<10:
    for vector1 in vector_array:
        for vector2 in vector_array:
            similarity = util.cos_sim(vector1, vector2)
            print(similarity)
            count += 1
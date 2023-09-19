from sentence_transformers import SentenceTransformer, util
import pandas as pd
from tqdm import tqdm
import numpy as np
import json

with open('./vector_data/webtoon_vectors_nospace.json', 'r') as json_file:
    data = json.load(json_file)

count = 0
for title in data:
    print(title)
    count += 1
    if count == 5:
        break
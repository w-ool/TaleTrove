from sentence_transformers import SentenceTransformer, util
import pandas as pd
from tqdm import tqdm

# model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
# sentence1 = ['무공에 미친 광마 이자하. 그는 마교 교주의 천옥을 훔쳐 쫓기던 중 벼랑에서 떨어지게 된다. 모든 게 끝났다고 생각한 순간 눈을 떠보니, 사람들에게 무시당하던 점소이 시절로 돌아와 있는데... 게다가 억울한 누명으로 두들겨 맞고 객잔은 박살이 나 있는 상황. 점소이 시절로 회귀한 광마! 사내는 다시 미치게 될 것인가? 아니면 사내의 적들이 미치게 될 것인가']
# sentence2 = ['흡혈귀와 요괴, 무당이 창궐한 혼란의 조선, 자신을 암흑어사라 칭하는 박문수가 타락한 관아를 파괴하고 다닌다. 다급해진 조정에서는 흡혈귀 왕의 부활을 노리는 암흑어사 박문수를 토벌하라 명하기 위해 갓 무과에 급제한 무관 안손에게 도술과 무술에 능한 도적 홍킬동을 찾아오라 태백산으로 파견한다.']
# vector1 = model.encode(sentence1)
# vector2 = model.encode(sentence2)
# similarities = util.cos_sim(vector1, vector2)
# print(vector1)
# print(similarities)

model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
webtoon_df = pd.read_csv('./naver_unfinished.csv')
stories = webtoon_df['story']
vectors = []

for story in tqdm(stories): # 580개 기준 48초
    vector = model.encode(story)
    vectors.append(vector)

webtoon_data = pd.DataFrame()
webtoon_data['title'] = webtoon_df['title']
webtoon_data['vector'] = vectors
for vector in webtoon_data['vector']:
    print(type(vector))
    break
# webtoon_data.to_csv('naver_incomplete_vector.csv', encoding='utf-8-sig')

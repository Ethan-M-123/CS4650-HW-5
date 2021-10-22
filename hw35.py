import spacy
import en_core_web_lg
from newsapi import NewsApiClient
nlp_eng = en_core_web_lg.load()
newsapi = NewsApiClient(api_key='449a66b6f6ea4532973919a154d18f32')


articles = [
    newsapi.get_everything(q='coronavirus', language='en', from_param='2021-09-22', to='2021-10-22', sort_by='relevancy', page=1),
    newsapi.get_everything(q='coronavirus', language='en', from_param='2021-09-22', to='2021-10-22', sort_by='relevancy', page=2),
    newsapi.get_everything(q='coronavirus', language='en', from_param='2021-09-22', to='2021-10-22', sort_by='relevancy', page=3),
    newsapi.get_everything(q='coronavirus', language='en', from_param='2021-09-22', to='2021-10-22', sort_by='relevancy', page=4),
    newsapi.get_everything(q='coronavirus', language='en', from_param='2021-09-22', to='2021-10-22', sort_by='relevancy', page=5)
]


import pandas as pd
dados = []

for i, page in enumerate(articles):
  for x in page['articles']:
    title = x['title']
    date = x['publishedAt']
    description = x['description']
    content = x['content']
    if (x['description'] == ''): description = " "
    dados.append({'title':title, 'date':date, 'desc':description, 'content':content})

    df = pd.DataFrame(dados)
    df = df.dropna()
    df.head()


import spacy
from spacy import glossary

def get_keywords_eng(text):
  doc = nlp_eng(text)
  result = []
  for token in doc:
    if (token.text in nlp_eng.Defaults.stop_words):
      continue
    if (token.pos_ in glossary.GLOSSARY):
      result.append(token.text)
  return result


from collections import Counter
results = []

for content in df.content.values:
  results.append([('#' + x[0]) for x in
Counter(get_keywords_eng(content)).most_common(5)])
  
df['keywords'] = results

df.to_csv(index=False)
import numpy as np
import pandas as pd 
import pickle 
import re
import spacy
import string

from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords

nlp = spacy.load('en_core_web_lg')

with open('../data/book_model', 'rb') as f:
    model = pickle.load(f)

book_list_df = pd.read_pickle('../data/book_list_df.pkl')

stop = stopwords.words('english')
stop_words_ = set(stopwords.words('english'))
wn = WordNetLemmatizer()

def keep_txt(token):
    return  token not in stop_words_ and token not in list(string.punctuation)  and len(token)>2   

def clean_txt(text):
    clean_text = []
    clean_text2 = []
    text = re.sub("'", "",text)
    text = re.sub("(\\d|\\W)+"," ",text)
    text = text.replace("kindle", "")
    text = text.replace("edition", "")
    clean_text = [ wn.lemmatize(word, pos="v") for word in word_tokenize(text.lower()) if keep_txt(word)]
    clean_text2 = [word for word in clean_text if keep_txt(word)]
    return " ".join(clean_text2)

reader_choices = ['monster', 'lore', 'grave', 'animal', 'dread', 'haunted', 'claw', 'eerie', 'old', 'mystery', 'dark', 'fear', 'ghost', 'terror', 'blood', 'gore', 'death', 'danger', 'atmosphere', 'supernatural']
import random
sample_reader = random.sample(reader_choices, 3)
reader_number = 1
dict = {'user_id': [reader_number], 'selections': [sample_reader]}
user_df = pd.DataFrame(dict)
user_df['text'] = user_df['selections'].map(str).apply(clean_txt)
user_recc_df = user_df[['user_id', 'text']]
u = 1
index = np.where(user_recc_df['user_id']==u)[0][0]
user_q = user_recc_df.iloc[[index]]
print(user_q)





def get_recommendation(top, book_list_df, scores):
  recommendation = pd.DataFrame(columns = ['title', 'score'])
  count = 0
  for i in top:
      recommendation.at[count, 'user_id'] = u
      recommendation.at[count, 'id'] = book_list_df['id'][i]
      recommendation.at[count, 'title'] = book_list_df['title'][i]
      recommendation.at[count, 'author'] = book_list_df['author'][i]
      recommendation.at[count, 'score'] =  scores[count]
      count += 1
  return recommendation

list_docs = []
for i in range(len(book_list_df)):
    doc = nlp("u'" + book_list_df['text'][i] + "'")
    list_docs.append((doc,i))
    

def calculateSimWithSpaCy(nlp, df, user_text, n=6):
    # Calculate similarity using spaCy
    list_sim =[]
    doc1 = nlp("u'" + user_text + "'")
    for i in df.index:
      try:
            doc2 = list_docs[i][0]
            score = doc1.similarity(doc2)
            list_sim.append((doc1, doc2, list_docs[i][1],score))
      except:
        continue

    return  list_sim

#restate the user's word choices "Based on the words you chose, user_q.text[0], your top 10 recommended books are..."

df3 = calculateSimWithSpaCy(nlp, book_list_df, user_q.text[0], n=10)
df_recom_spacy = pd.DataFrame(df3).sort_values([3], ascending=False).head(10)
df_recom_spacy.reset_index(inplace=True)

index_spacy = df_recom_spacy[2]
list_scores = df_recom_spacy[3]

print(get_recommendation(index_spacy, book_list_df, list_scores))
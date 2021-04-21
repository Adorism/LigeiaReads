import numpy as np
import pandas as pd
import spacy 
import nltk
import sklearn
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords

nlp = spacy.load('en_core_web_lg')
book_list = pd.read_pickle('../data/scary_books.pkl')

book_list['stars']=book_list['stars'].fillna(book_list['stars'].mean())
book_list['customer_reviews']=book_list['customer_reviews'].fillna(0)
book_list['publisher']=book_list['publisher'].fillna('Self')

book_list["id"] = book_list.index + 1
book_list["text"] = book_list["title"].map(str) + " " + book_list["author"] +" "+ book_list["description"]+ " "+book_list['publisher']
book_list_df = book_list[['id', 'text', 'title']]


stop = stopwords.words('english')
stop_words_ = set(stopwords.words('english'))
wn = WordNetLemmatizer()

def black_txt(token):
    return  token not in stop_words_ and token not in list(string.punctuation)  and len(token)>2   

def clean_txt(text):
    clean_text = []
    clean_text2 = []
    text = re.sub("'", "",text)
    text = re.sub("(\\d|\\W)+"," ",text)
    text = text.replace("kindle", "")
    text = text.replace("edition", "")
    clean_text = [ wn.lemmatize(word, pos="v") for word in word_tokenize(text.lower()) if black_txt(word)]
    clean_text2 = [word for word in clean_text if black_txt(word)]
    return " ".join(clean_text2)

book_list_df['text'] = book_list_df['text'].apply(clean_txt)

reader_choices = ['monster', 'lore', 'grave', 'animal', 'dread', 'haunted', 'claw', 'eerie', 'old', 'mystery', 'dark', 'fear', 'ghost', 'terror', 'blood', 'gore', 'death', 'danger', 'atmosphere', 'supernatural']
import random
sample_reader = random.sample(reader_choices, 3)

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
    print(len(list_docs))

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

get_recommendation(index_spacy, book_list_df, list_scores)

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
from sklearn.feature_extraction.text import TfidfVectorizer

import pickle

nlp = spacy.load('en_core_web_lg')
book_list = pd.read_pickle('../data/scary_books.pkl')

book_list['stars']=book_list['stars'].fillna(book_list['stars'].mean())
book_list['customer_reviews']=book_list['customer_reviews'].fillna(0)
book_list['publisher']=book_list['publisher'].fillna('Self')

book_list["id"] = book_list.index + 1
book_list["text"] = book_list["title"].map(str) + " " + book_list["author"] +" "+ book_list["description"]+ " "+book_list['publisher']
book_list_df = book_list[['id', 'text', 'title', 'author', 'url']]
book_list_df.to_pickle('../data/book_list_df.pkl')

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

#initializing tfidf vectorizer

tfidf_vectorizer = TfidfVectorizer()
book_model = tfidf_vectorizer.fit_transform((book_list_df['text'])) #fitting and transforming the vector

with open('book_model', 'wb') as f:
    pickle.dump(book_model, f)
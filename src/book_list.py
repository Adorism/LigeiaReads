import numpy as np
import pandas as pd

#load the dataset, consisting of just under 50000 books representing all genres
df = pd.read_csv('../data/amazon_books.csv')

rec_df = df[['title', 'author', 'description', 'publisher', 'customer_reviews', 'stars', 'url']].copy()
#Remove titles with no publisher listed because those titles tended to be either about writing or about a book, rather than being a narrative work
rec_df.dropna(subset=['publisher'])

#accumulate books based on words included in the description text
horror_books = rec_df.loc[rec_df['description'].str.contains("horror", case=False)]
terror_books = rec_df.loc[rec_df['description'].str.contains("terrifying", case=False)]
supernatural_books = rec_df.loc[rec_df['description'].str.contains("supernatural", case=False)]
scream_books = rec_df.loc[rec_df['description'].str.contains("scream", case=False)]
ghost_books = rec_df.loc[rec_df['description'].str.contains("ghostly", case=False)]
morbid_books = rec_df.loc[rec_df['description'].str.contains("morbid", case=False)]
gore_books = rec_df.loc[rec_df['description'].str.contains("gruesome", case=False)]
rec_df = pd.concat([horror_books, supernatural_books, terror_books, scream_books, ghost_books, morbid_books, gore_books]).drop_duplicates().reset_index(drop=True)


#pickle this dataframe to use in classifier
rec_df.to_pickle('../data/scary_books.pkl')
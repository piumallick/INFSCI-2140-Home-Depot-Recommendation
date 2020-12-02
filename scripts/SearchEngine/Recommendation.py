# Importing the necessary Libraries
import Classes.Path as Path
import pandas as pd
import pathlib
import numpy as np
# %matplotlib inline
import re
import string
import pickle
import sys

import nltk

pd.set_option('display.max_colwidth', None)

# from Main import get_pickle_file

nltk.download('stopwords')
nltk.download('wordnet')

from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.decomposition import TruncatedSVD,LatentDirichletAllocation
from sklearn.metrics.pairwise import linear_kernel




def get_pickle_file():
    root = pathlib.Path(__file__).parent.parent.__str__()

    # We will select only 20000 rows for our demo purpose
    pickle_in = open(root + Path.InputPickleFile, "rb")
    product_df = pickle.load(pickle_in)
    product_df = product_df[1:20001]
    return product_df

def calculate_tfidf():
    # Define a TF-IDF Vectorizer Object.
    # Remove all english stop words such as 'the', 'a', etc.
    tfidf = TfidfVectorizer(stop_words='english')

    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(get_pickle_file()['description_words'])

    # Output the shape of tfidf_matrix
    return tfidf_matrix

def calculate_cosine_similarity_matrix():
    cosine_sim = linear_kernel(calculate_tfidf(), calculate_tfidf())
    return cosine_sim

def create_indices():
    # Construct a reverse map of indices and product titles
    indices = pd.Series(get_pickle_file().index,
                        index=get_pickle_file()['product_title']).drop_duplicates()
    return indices

# Function that takes in product title as input and outputs most similar products

def get_recommendations(query, cosine_sim=calculate_cosine_similarity_matrix()):
    # cosine_sim = calculate_cosine_similarity_matrix()
    # Get the index of the product that matches the query

    # gettin the index of the movie that matches the title
    idx = create_indices()[query]

    # Get the pairwsie similarity scores of all products with that product
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the product based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar product
    sim_scores = sim_scores[1:15]

    # Get the product indices
    product_indices = [i[0] for i in sim_scores]

    df = get_pickle_file()['product_title'].iloc[product_indices]
    # Return the top 10 most similar products
    return df

df = get_recommendations(sys.argv[1], calculate_cosine_similarity_matrix())

df = pd.DataFrame(data=df)
df = df["product_title"].str.split("", n = 1, expand = True)
df["product_uid"] = df.index
df = df.rename(columns={1: "product_title"})
df.drop(columns = 0)
result_json= df.to_json(orient = "records")
print(result_json)

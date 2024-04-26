import math 
import pandas as pd
from rank_bm25 import BM25Okapi
import numpy as np


def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    r = 3958.8
    distance = r * c
    return distance

def get_documents_within_25miles(df, latitude, longitude):
    locations_within_25km = df[df.apply(lambda row: calculate_distance(latitude, longitude, row['latitude'], row['longitude']), axis=1) < 25]
    return locations_within_25km


def retrieval_info(data, bm25, query, latitude ,longitude):
    
    query_tokens = query.split(" ")
    # Get document scores
    doc_scores = bm25.get_scores(query_tokens)
    data['doc_scores'] = doc_scores
    
    docs = get_documents_within_25miles(data,latitude,longitude)
    
    sorted_docs = docs.sort_values(by=['doc_scores', 'avg_rating'], ascending=[False, False])
    # sorted_docs = sorted_docs.drop(columns=['doc_information', 'MISC','text'])
    top_10_docs = sorted_docs.head(10)
    search_info = top_10_docs.to_dict(orient='records')

    return search_info

def recommender_info(data, gmap_id):

    recommender_matrix = pd.read_pickle('recommendation.pickle')
    row = recommender_matrix.loc[gmap_id].to_list()

    recom_info={}
    for id in row:
        recom_info[id] = data.loc[data['gmap_id'] == id]

    return recom_info




    

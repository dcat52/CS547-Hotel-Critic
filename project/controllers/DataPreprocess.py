from project.models.Hotel import Hotel
from project.controllers.PorterStemmer import *
import glob
import json
import math
from statistics import mean
import re
import os
from collections import Counter
# from collections import Counter

# bt = binarytree.binary_tree()
# # contains hotel names
# hotels = []

# def crawl_tree(node, term):
#     if not node: return set()
#     if ('*' in term and node.key.startswith(term[:-1])) or term == node.key:
#         x = node.data
#     else: x = set()
#     return x.union(crawl_tree(node.left, term)).union(crawl_tree(node.right, term))

def build_hotel_obj_data(pattern='./json_small/*.json') -> list:
    """
    build a list of hotel objects

    Args:
        pattern (str, optional): pattern of matching json files. Defaults to './json_small/*.json'.

    Returns:
        list: list of Hotel objects
    """
    hotel_list = []

    for file in glob.glob(pattern):
        hotel = Hotel()
        parse_hotel_id(hotel, file)
        data = load_datafile(file)
        if parse_hotel_info(hotel, data) and generate_rating_dict(hotel, data):
            us = calculate_universal_score(hotel)
            hotel_list.append(hotel)
    hotel_list = sorted(hotel_list, key=lambda x: x.us , reverse= True)

    return hotel_list

def build_hotel_review_data(pattern='./json_small/*.json') -> list:
    """
    build a dict of hotel id, review list pairs

    Args:
        pattern (str, optional): pattern of matching json files. Defaults to './json_small/*.json'.

    Returns:
        dict: dictionary of { hotel_id : ['review 1 contents', 'review 2 contents'] }
    """
    hotel_dict = {}

    for file in glob.glob(pattern):
        hotel = Hotel()
        parse_hotel_id(hotel, file)
        hotel_id = hotel.id

        data = load_datafile(file)
        if parse_hotel_info(hotel, data) and generate_rating_dict(hotel, data):
            reviews = parse_hotel_reviews(data)
            hotel_dict[hotel_id] = reviews

    return hotel_dict

def parse_hotel_id(hotel: Hotel, filepath: str) -> bool:
    """
    get the hotel id number from the filename

    Args:
        hotel (Hotel): hotel object
        filepath (str): path to json file

    Returns:
        bool: whether successful
    """
    hotel_id = os.path.basename(filepath)
    hotel.id = hotel_id[:-5]

    return True
    
def parse_hotel_info(hotel: Hotel, hotel_dict: dict) -> bool:
    """
    Parses hotel info

    Args:
        hotel (Hotel): hotel object
        hotel_dict (dict): hotel json data

    Returns:
        bool: whether the parsing was sucessful
    """

    try:
        hotel_info = hotel_dict['HotelInfo']
        hotel.name = hotel_info['Name']
        hotel.address = hotel_info['Address']
        hotel.price = hotel_info.get('Price', '')
    except Exception as e:
        # print(e)
        return False

    return True

def generate_rating_dict(hotel, hotel_dict):
    """
    Parses the hotel review information

    Args:
        hotel (Hotel): hotel object
        hotel_dict (dict): hotel json data

    Returns:
        bool: whether the rating was generated successfully
    """
    avg_rating = {}
    try:
        hotel.num_of_reviews = len(hotel_dict['Reviews'])
        for review in hotel_dict['Reviews']:
            for aspect in review['Ratings'].keys():
                if aspect in avg_rating:
                    review_aspect_rating = int(float(review['Ratings'][aspect]))
                    if review_aspect_rating >= 0:
                        avg_rating[aspect][0] += review_aspect_rating
                        avg_rating[aspect][1] += 1
                else:
                    review_aspect_rating = int(float(review['Ratings'][aspect]))
                    if review_aspect_rating >= 0:
                        avg_rating[aspect] = [review_aspect_rating, 1]

        for k in avg_rating:
            temp_avg_rating = avg_rating[k][0] / avg_rating[k][1]
            avg_rating[k] = round(temp_avg_rating, 2)
        hotel.avg_rating = avg_rating
    except Exception as e:
        # print(e)
        # traceback.print_exc()
        return False

    return True

def parse_hotel_reviews(data: dict) -> list:
    """
    parse hotel reviews from data

    Args:
        data (dict): hotel json dict

    Returns:
        list: series of reviews
    """

    all_reviews = []

    reviews = data.get('Reviews')
    for r in reviews:
        text = r.get('Content', '')
        all_reviews.append(text)

    return all_reviews

# def index_dir(hotel_list):
#     idx = index_dir(hotel_list, bt, hotels)    
#     print("indexed %d hotels" % idx)
#     return hotel_list

def index_dir(hotel_list, bt, hotels):
        num_hotels_indexed = 0
        for h in hotel_list:
            num_hotels_indexed += 1
            if h.name not in hotels:
                hotels.append(h.name)
            hotel_idx = hotels.index(h.name)
            for term in h.comment:
                tf = h.comment.count(term)
                weighted_tf = 1 + math.log10(tf)
                if term not in bt:
                    bt[term] = set()
                if hotel_idx not in bt[term]:
                    bt[term].add((hotel_idx, weighted_tf, len(h.comment)))
                    
        return num_hotels_indexed


def load_datafile(filepath):
    """
    Load json data from hotel file

    Args:
        filepath (str): hotel specific json file

    Returns:
        dict: hotel json data
    """
    with open(filepath) as f:
        hotel_dict = json.load(f)
    return hotel_dict

def tokenize(text):
    clean_string = re.sub('[^a-z0-9 ]', ' ', text.lower())
    tokens = clean_string.split()
    return tokens

def stemming(tokens):
    stemmed_tokens = []
    # PUT YOUR CODE HERE
    st = PorterStemmer()
    for w in tokens:
        stemmed_tokens.append(st.stem(w,0,len(w)-1))
    return stemmed_tokens

def calculate_universal_score(hotel, overall_weight=0.5, other_weight=0.45, num_review_weight=0.05):
    len_aspects = len(hotel.avg_rating) -1 if 'Overall' in hotel.avg_rating else len(hotel.avg_rating)
    aspects = []
    for k in hotel.avg_rating:
        if k != 'Overall':
            aspects.append(k)

    # retrieve overall rating from the avg_rating dictionary, otherwise use all other aspects' average score as overall rating
    overall = hotel.avg_rating['Overall'] if 'Overall' in hotel.avg_rating else mean(hotel.avg_rating.values())
    # if there is no other aspects score then overall weight becomes 0.95
    overall_score = overall_weight * overall if len_aspects > 0 else (overall_weight+other_weight) * overall 
    other_weight = (other_weight / len_aspects) if len_aspects > 0 else other_weight
    other_score = 0
    if len_aspects > 0:
        for k in aspects:
            other_score += hotel.avg_rating[k] * other_weight
    final_score = overall_score + other_score + (math.log(hotel.num_of_reviews)*num_review_weight)
    hotel.us = final_score
    return final_score


def build_tf_data(hotel_obj_list,review_data):
    tf_d = {}
    count = 0
    for ho in hotel_obj_list:
        count += 1
        print(count)
        hotel_id = ho.id
        tokens = tokenize(' '.join(review_data[hotel_id]))
        stem_tokens = stemming(tokens)
        tf_d[hotel_id] = dict(Counter(stem_tokens))
    return tf_d

def build_idf_data(hotel_obj_list, tf_data):
    idf_list = []
    for ho in hotel_obj_list:
        idf_list.extend(list(tf_data[ho.id].keys()))
    print(idf_list[:10])
    return Counter(idf_list)

    

        
    

    

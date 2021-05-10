from project.models.Hotel import Hotel
from project.controllers.QueryProcess import *
import pandas as pd
import glob
import json
import math
import re
import os
import traceback

# bt = binarytree.binary_tree()
# # contains hotel names
# hotels = []

def crawl_tree(node, term):
    if not node: return set()
    if ('*' in term and node.key.startswith(term[:-1])) or term == node.key:
        x = node.data
    else: x = set()
    return x.union(crawl_tree(node.left, term)).union(crawl_tree(node.right, term))

def build_hotel_obj_data(pattern='./json_small/*.json') -> list:
    hotel_list = []

    for file in glob.glob(pattern):
        hotel = Hotel()
        parse_hotel_id(hotel, file)
        data = load_datafile(file)
        if parse_hotel_info(hotel, data) and generate_rating_dict(hotel, data):
            hotel_list.append(hotel)

    return hotel_list

def build_hotel_review_data(pattern='./json_small/*.json') -> list:
    hotel_dict = {}

    for file in glob.glob(pattern):
        term_freqs = {}
        hotel = Hotel()
        parse_hotel_id(hotel, file)
        hotel_id = hotel.id[:-5]

        data = load_datafile(file)
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
    hotel.id = hotel_id

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
    return set(tokens)

def stemming(tokens):
    stems = set()
    p = PorterStemmer.PorterStemmer()
    for token in tokens:
        stems.add(p.stem(token, 0, len(token) - 1))
    return stems

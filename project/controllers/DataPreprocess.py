from project.models.Hotel import Hotel
from project.controllers.QueryProcess import *
import pandas as pd
import glob
import json
import math
import re

def build_data(bt, hotels, pattern='./json_small/*.json'):
    hotel_list = []

    for file in glob.glob(pattern):
        data = load_datafile(file)
        hotel = Hotel()
        if generate_hotel_name(hotel, data) is not None and generate_rating_dict(hotel, data) is not None:
            hotel_list.append(hotel)
    idx = index_dir(hotel_list, bt, hotels)    
    print("indexed %d hotels" % idx)
    return hotel_list

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

def generate_rating_dict(hotel, hotel_dict):
    """
    Parses the hotel review information

    Args:
        hotel (Hotel): hotel object
        hotel_dict (dict): hotel json data

    Returns:
        float: average rating for the hotel
    """
    avg_rating = {}
    if 'Reviews' in hotel_dict:
        hotel.num_of_reveiws = len(hotel_dict['Reviews'])
        for review in hotel_dict['Reviews']:
            if 'Ratings' in review:
                for aspect in review['Ratings'].keys():
                    if aspect in avg_rating:
                        avg_rating[aspect][0] += abs(int(float(review['Ratings'][aspect])))
                        avg_rating[aspect][1] += 1
                    else:
                        avg_rating[aspect] = [int(float(review['Ratings'][aspect])),1]
            if 'Content' in review:
               tokens = tokenize(review['Content'])
               hotel.comment += tokens 
    for k in avg_rating:
        avg_rating[k] = round(avg_rating[k][0] / avg_rating[k][1],2)
    hotel.avg_rating = avg_rating
    return avg_rating

def tokenize(text):
    clean_string = re.sub('[^a-z0-9 ]', ' ', text.lower())
    tokens = clean_string.split()
    return tokens
    
def generate_hotel_name(hotel, hotel_dict):
    """
    Parses hotel name information

    Args:
        hotel (Hotel): hotel object
        hotel_dict (dict): hotel json data

    Returns:
        str: the name or substitute for the name of hotel
    """
    if 'HotelInfo' in hotel_dict:
        hotel_info = hotel_dict['HotelInfo']
        if 'Name' in hotel_info:
            hotel.name = hotel_info['Name']
        if "Price" in hotel_info:
            hotel.price = hotel_info['Price']
        if 'Address' in hotel_info:
            hotel.address = hotel_info['Address']
            return hotel_info['Name']
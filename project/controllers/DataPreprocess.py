from project.models.Hotel import Hotel
from project.controllers.QueryProcess import *

import pandas as pd
import glob
import json
import re

def build_data(pattern='./json_small/*.json'):
    hotel_list = []

    for file in glob.glob(pattern):
        data = load_datafile(file)
        hotel = Hotel()
        if generate_hotel_name(hotel, data) is not None and generate_rating_dict(hotel, data) is not None:
            hotel_list.append(hotel)
        
    return hotel_list

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
    for k in avg_rating:
        avg_rating[k] = round(avg_rating[k][0] / avg_rating[k][1],2)
    hotel.avg_rating = avg_rating
    return avg_rating

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
            return hotel_info['Name']

def calculate_aspect_score(hotel, aspects, main_weight=0.6, overall_weight=0.2, other_weight=0.1, num_review_weight=0.1):
    len_dict = len(hotel.avg_rating)
    len_aspects = 0
    real_aspects = []
    # find out aspects that are in the query and match them with the rating dictionary
    for aspect in aspects:
        if aspect in hotel.avg_rating:
            real_aspects.append(aspect)
    len_aspects = len(real_aspects)
    # if the aspect
    if len_aspects == 0:
        main_weight = 0
        overall_weight = 0.8
    else:
        main_weight = main_weight / len_aspects
    other_weight = other_weight / (len_dict - len_aspects) if 'Overall' not in hotel.avg_rating else other_weight / ((len_dict - len_aspects) - 1)
    other_weight_score = 0
    main_weight_score = 0
    overall_weight_score = 0

    for k in hotel.avg_rating:
        if 'Overall' in hotel.avg_rating:
            if k not in set(real_aspects) and k != 'Overall':
                other_weight_score += hotel.avg_rating[k] * other_weight
        else:
            if k not in set(real_aspects):
                other_weight_score += hotel.avg_rating[k] * other_weight
                overall_weight_score += hotel.avg_rating[k]
    overall_weight_score = overall_weight_score / ((len_dict - len_aspects) - 1)

    for a in real_aspects:
        main_weight_score += hotel.avg_rating[a] * main_weight

    if 'Overall' in hotel.avg_rating:
        final_score = main_weight_score + other_weight_score + (hotel.avg_rating['Overall'] * overall_weight) + (num_review_weight * hotel.num_of_reveiws)
    else:
        final_score = main_weight_score + other_weight_score + (overall_weight_score * overall_weight) + (num_review_weight * hotel.num_of_reveiws)
    return final_score

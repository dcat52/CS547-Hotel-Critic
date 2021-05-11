import pandas as pd
import json
import re
import numpy as np
import math 
from project.controllers.DataPreprocess import *
from statistics import mean
from collections import Counter

# def crawl_tree(node, term):
#     if not node: return set()
#     if term == node.key:
#         x = node.data
#     else: x = set()
#     return x.union(crawl_tree(node.left, term)).union(crawl_tree(node.right, term))

# def cosine(q, n):
#     # n is the length of list of hotel names that need to be passed in
#     length = np.zeros(n)
#     scores = np.zeros(n)
#     tokens = tokenize(q)
#     for t in tokens:
#         hotels = crawl_tree(bt.root, t)
#         tf = tokens.count(t)
#         weighted_tf = 1 + math.log10(tf)
#         idf = math.log10(n // len(hotels))
#         q_tf_idf = weighted_tf * idf
#         for hotel in hotels:
#             h_tf_idf = hotel[1] * idf
#             scores[hotel[0]] += q_tf_idf * h_tf_idf
#             length[hotel[0]] = hotel[2]
#     for i in range(len(scores)):
#         scores[i] //= length[i] 
#     return scores[:10]

def rank_aspect(hotel, text):
    # process and first, then or later
    or_score = []
    if 'or' in text:
        processd_text = text.split('or')
        for term in processd_text:
            # if sub-query includes and
            if 'and' in term:
                key_words = hotel.process_and(term)
                # calculate weighted score
                score = hotel.calculate_aspect_score(key_words)
                or_score.append(score)
            # process each non-and sub-query one by one
            else:
                term = term.strip()
                key_words = hotel.process_word(term)
                score = hotel.calculate_aspect_score(key_words)
                or_score.append(score)
    # process each non-and sub-query one by one
    else:
        terms = text
        key_words = process_word(hotel, terms)
        score = calculate_aspect_score(hotel, key_words)
        or_score.append(score)

    return round(max(or_score),2)

def process_word(hotel, text):
    key_words_dict = {'service':'Service','clean':'Cleanliness','overall':'Overall','value':'Value','sleep quality':'Sleep Quality','room':'Rooms','location':'Location','internet':'Business service (e.g., internet access)','check in':'Check in / front desk'}
    terms = text.split(' ')
    aspects = []
    for term in terms:
        if term in key_words_dict:
            aspects.append(key_words_dict[term])
    return aspects

def process_and(hotel, text):
    key_words_dict = {'service':'Service','clean':'Cleanliness','overall':'Overall','value':'Value','sleep quality':'Sleep Quality','room':'Rooms','location':'Location','internet':'Business service (e.g., internet access)','check in':'Check in / front desk'}
    aspect = []
    remove_and = text.split('and')
    for term in remove_and:
        term = term.strip()
        for t in term.split(' '):
            # get all aspect words
            if t.strip() in key_words_dict:
                aspect.append(key_words_dict[t.strip()])
    return aspect


def parse_location(hotel_obj_list, location):
    matched_hotels = []
    for obj in hotel_obj_list:
        if location.lower() in obj.address.lower():
            matched_hotels.append(obj)
    if len(matched_hotels) >= 200:
        matched_hotels = matched_hotels[:200]
    elif len(location) == 0:
        matched_hotels = hotel_obj_list[:200]


    return matched_hotels


def cal_cosine(hotel, review_tf, text):
    text = text.lower()
    text = text.split(' ')
    stem_text = stemming(text)
    text_tf_d = Counter(stem_text)
    matched_text = []  
    add_hotel = 0
    add_text = 0
    for t in stem_text:
        if t in review_tf[hotel.id]:
            hotel_tf = review_tf[hotel.id][t]
            text_tf = text_tf_d[t]
            add_hotel += hotel_tf ** 2
            add_text += text_tf ** 2
            matched_text.append((t,hotel_tf,text_tf))
    result = {}
    for m in matched_text:
        result[m[0]] = (m[1]/math.sqrt(add_hotel))*(m[2]/math.sqrt(add_text))
    return sum(result.values())




def calculate_aspect_score(hotel, aspects, main_weight=0.6, us_weight = 0.4):

    us = calculate_universal_score(hotel)

    real_aspects = []
    # find out aspects that are in the query and match them with the rating dictionary
    for aspect in aspects:
        if aspect in hotel.avg_rating and aspect != 'overall':
            real_aspects.append(aspect)
    if len(real_aspects) > 0:
        main_weight = main_weight / len(real_aspects)
        main_score = 0
        for ra in real_aspects:
            main_score += hotel.avg_rating[ra] * main_weight
        final_score = main_score + us_weight * hotel.us 
    else:
        final_score = hotel.us         

    return final_score

def cal_final_score(hotel, text, review_tf):
    rated_score = rank_aspect(hotel, text)
    review_score = cal_cosine(hotel, review_tf, text)*5
    final_score = rated_score + review_score
    return round(final_score,3)
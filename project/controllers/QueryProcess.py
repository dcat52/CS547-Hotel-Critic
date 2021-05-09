import pandas as pd
import json
import re
import numpy as np
import math 
from project.controllers.DataPreprocess import *
from statistics import mean

def crawl_tree(node, term):
    if not node: return set()
    if term == node.key:
        x = node.data
    else: x = set()
    return x.union(crawl_tree(node.left, term)).union(crawl_tree(node.right, term))

def cosine(q, n):
    # n is the length of list of hotel names that need to be passed in
    length = np.zeros(n)
    scores = np.zeros(n)
    tokens = tokenize(q)
    for t in tokens:
        hotels = crawl_tree(bt.root, t)
        tf = tokens.count(t)
        weighted_tf = 1 + math.log10(tf)
        idf = math.log10(n // len(hotels))
        q_tf_idf = weighted_tf * idf
        for hotel in hotels:
            h_tf_idf = hotel[1] * idf
            scores[hotel[0]] += q_tf_idf * h_tf_idf
            length[hotel[0]] = hotel[2]
    for i in range(len(scores)):
        scores[i] //= length[i] 
    return scores[:10]

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
    terms = text.split(' ')
    aspects = []
    for term in terms:
        if term in hotel.key_words:
            aspects.append(hotel.key_words[term])
    return aspects

def process_and(hotel, text):
    aspect = []
    remove_and = text.split('and')
    for term in remove_and:
        term = term.strip()
        for t in term.split(' '):
            # get all aspect words
            if t.strip() in hotel.key_words:
                aspect.append(hotel.key_words[t.strip()])
    return aspect

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
    final_score = overall_score + other_score + (math.log(hotel.num_of_reveiws)*num_review_weight)
    hotel.us = final_score
    return final_score


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

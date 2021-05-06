import pandas as pd
import json
import re

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
    for term in terms:
        if term in hotel.key_words:
            return [hotel.key_words[term]]
    return []

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

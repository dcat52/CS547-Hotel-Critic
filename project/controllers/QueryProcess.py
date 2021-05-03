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
        key_words = process_word(terms)
        score = hotel.calculate_aspect_score(key_words)
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

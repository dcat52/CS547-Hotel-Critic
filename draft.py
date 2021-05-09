import pandas as pd 
import glob 
import json
import re 
import math 
from statistics import mean 
class Hotel(object):

    def __init__(self):
        self.num_of_reveiws = 0
        self.avg_rating = {}
        self.name = ''
        self.address = ''
        self.city = ''
        self.state = ''
        self.us = 0
        self.address = ''
        self.price = ''
        self.key_words = {'service':'Service','clean':'Cleanliness','overall':'Overall','value':'Value','sleep quality':'Sleep Quality','room':'Rooms','location':'Location','internet':'Business service (e.g., internet access)','check in':'Check in / front desk'}


    def generate_rating_dict(self,filepath):
        avg_rating = {}
        with open(filepath) as f:
            hotel_dict = json.load(f)
            if 'Reviews' in hotel_dict:
                self.num_of_reveiws = len(hotel_dict['Reviews'])
                for review in hotel_dict['Reviews']:
                    if 'Ratings' in review:
                        for aspect in review['Ratings'].keys():
                            if aspect in avg_rating:
                                avg_rating[aspect][0] += abs(int(float(review['Ratings'][aspect])))
                                avg_rating[aspect][1] += 1
                            else:
                                avg_rating[aspect] = [int(float(review['Ratings'][aspect])),1]
        for k in avg_rating:
            avg_rating[k] = round(avg_rating[k][0]/avg_rating[k][1],2)
        self.avg_rating = avg_rating
        return avg_rating


    def generate_hotel_name(self,filepath):
        with open(filepath) as f:
            hotel_dict = json.load(f)
            if 'HotelInfo' in hotel_dict:
                hotel_info = hotel_dict['HotelInfo']
                if 'Name' in hotel_info:
                    self.name = hotel_info['Name']
                    if "Price" in hotel_info:
                        self.price = hotel_info['Price']
                    if 'Address' in hotel_info:
                        self.address = hotel_info['Address']
                    return hotel_info['Name']

    def rank_aspect(self,text):
        # process and first, then or later
        or_score = []
        if 'or' in text:
            processd_text = text.split('or')
            for term in processd_text:
                # if sub-query includes and
                if 'and' in term:
                    key_words = self.process_and(term)
                    # calculate weighted score
                    score = self.calculate_aspect_score(key_words)
                    or_score.append(score)
                # process each non-and sub-query one by one
                else:
                    term = term.strip()
                    key_words = self.process_word(term)
                    score = self.calculate_aspect_score(key_words)
                    or_score.append(score)
        # process each non-and sub-query one by one
        else:
            terms = text
            key_words = self.process_word(terms)
            print(key_words)
            score = self.calculate_aspect_score(key_words)
            or_score.append(score)

        return round(max(or_score),2)


    def tokenize(self, text, is_search=False):
        if is_search:
            # don't strip out our wildcard character from query terms
            clean_string = re.sub('[^a-z0-9 *]', ' ', text.lower())
        else:
            clean_string = re.sub('[^a-z0-9 ]', ' ', text.lower())
        tokens = clean_string.split()
        return tokens


    def process_word(self,text):
        terms = text.split(' ')
        aspects = []
        for term in terms:
            if term in self.key_words:
                aspects.append(self.key_words[term])
        return aspects


    def process_and(self,text):
        aspect = []
        remove_and = text.split('and')
        for term in remove_and:
            term = term.strip()
            for t in term.split(' '):
                # get all aspect words
                if t.strip() in self.key_words:
                    aspect.append(self.key_words[t.strip()])
        return aspect


    def calculate_universal_score(self, overall_weight=0.5, other_weight=0.45, num_review_weight=0.05):
        len_aspects = len(self.avg_rating) -1 if 'Overall' in self.avg_rating else len(self.avg_rating)

        aspects = []
        for k in self.avg_rating:
            if k != 'Overall':
                aspects.append(k)

        # retrieve overall rating from the avg_rating dictionary, otherwise use all other aspects' average score as overall rating
        overall = self.avg_rating['Overall'] if 'Overall' in self.avg_rating else mean(self.avg_rating.values())
        # if there is no other aspects score then overall weight becomes 0.95
        overall_score = overall_weight * overall if len_aspects > 0 else (overall_weight+other_weight) * overall 
        other_weight = (other_weight / len_aspects) if len_aspects > 0 else other_weight
        other_score = 0
        if len_aspects > 0:
            for k in aspects:
                other_score += self.avg_rating[k] * other_weight
        final_score = overall_score + other_score + (math.log(self.num_of_reveiws)*num_review_weight)
        self.us = final_score
        return final_score



    def calculate_aspect_score(self,aspects,main_weight=0.6, us_weight = 0.4):
        print(aspects)

        us = self.calculate_universal_score()

        real_aspects = []
        # find out aspects that are in the query and match them with the rating dictionary
        for aspect in aspects:
            if aspect in self.avg_rating and aspect != 'overall':
                real_aspects.append(aspect)
        if len(real_aspects) > 0:
            main_weight = main_weight / len(real_aspects)
            main_score = 0
            for ra in real_aspects:
                main_score += self.avg_rating[ra] * main_weight
            final_score = main_score + us_weight * self.us 
        else:
            final_score = self.us         

        return final_score


def main(args):
    hotel = Hotel()
    print("start processing hotel ratings")
    text = 'internet'
    hotel_score = []
    for file in glob.glob('./json_small/*.json'):
        if hotel.generate_hotel_name(file) != None and hotel.generate_rating_dict(file) != None:
            name = hotel.name
            price = hotel.price
            addrs = hotel.address
            print(name,price,addrs)
            # score = hotel.rank_aspect(text)
            # combo = (name,score)
            # hotel_score.append(combo)
    # hotel_score = sorted(hotel_score, key = lambda x: x[1],reverse=True) 
    # print(hotel_score)
    # print(hotel.name)
   

if __name__ == '__main__':
    import sys 
    main(sys.argv)


        

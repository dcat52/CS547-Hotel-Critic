import pandas as pd 
import glob 
import json
import re 


class Hotel(object):

    def __init__(self):
        self.num_of_reveiws = 0
        self.avg_rating = {}
        self.name = ''
        self.address = ''
        self.city = ''
        self.state = ''
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
                    return hotel_info['Name']

    def rank_aspect(self,text):
        # process and first, then or later
        or_score = []
        if 'or' in text:
            processd_text = text.split('or')
            for term in processd_text:
                if 'and' in term:
                    key_words = self.process_and(term)
                    score = self.calculate_aspect_score(key_words)
                    or_score.append(score)
                else:
                    term = term.strip()
                    key_words = self.process_or(term)
                    score = self.calculate_aspect_score(key_words)
                    or_score.append(score)
        else:
            terms = text
            key_words = self.process_or(terms)
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


    def process_or(self,text):
        terms = text.split(' ')
        for term in terms:
            if term in self.key_words:
                return [self.key_words[term]]


    def process_and(self,text):
        aspect = []
        remove_and = text.split('and')
        for term in remove_and:
            term = term.strip()
            for t in term.split(' '):
                if t.strip() in self.key_words:
                    aspect.append(self.key_words[t.strip()])
        return aspect


    def calculate_aspect_score(self,aspects,main_weight=0.6, overall_weight=0.2, other_weight=0.1, num_review_weight=0.1):
        len_dict = len(self.avg_rating)
        real_aspects = []
        for aspect in aspects:
            if aspect in self.avg_rating:
                real_aspects.append(aspect)
        len_aspects = len(real_aspects)
        if len_aspects == 0:
            main_weight = 0
        else:
            main_weight = main_weight/len_aspects
        other_weight = other_weight/(len_dict-len_aspects) if 'Overall' not in self.avg_rating else other_weight/((len_dict-len_aspects)-1)
        other_weight_score = 0
        main_weight_score = 0
        overall_weight_score = 0
        for k in self.avg_rating:
            if 'Overall' in self.avg_rating:
                if k not in set(real_aspects) and k != 'Overall':
                    other_weight_score += self.avg_rating[k]*other_weight
            else:
                if k not in set(real_aspects):
                    other_weight_score += self.avg_rating[k]*other_weight
                    overall_weight_score += self.avg_rating[k]
        overall_weight_score = overall_weight_score/other_weight

        for a in real_aspects:
            main_weight_score += self.avg_rating[a]*main_weight

        if 'Overall' in self.avg_rating:
            final_score = main_weight_score + other_weight_score + (self.avg_rating['Overall'] * overall_weight) + (num_review_weight * self.num_of_reveiws)
        else:
            final_score = main_weight_score + other_weight_score + (overall_weight_score * overall_weight) + (num_review_weight * self.num_of_reveiws)
        return final_score


def main(args):
    hotel = Hotel()
    print("start processing hotel ratings")
    text = 'clean'
    hotel_score = []
    for file in glob.glob('./json_small/*.json'):
        if hotel.generate_hotel_name(file) != None and hotel.generate_rating_dict(file) != None:
            key = hotel.generate_hotel_name(file)
            content = hotel.rank_aspect(text)
            combo = (key,content)
            hotel_score.append(combo)
    hotel_score = sorted(hotel_score, key = lambda x: x[1],reverse=True) 
    print(hotel_score)
   

if __name__ == '__main__':
    import sys 
    main(sys.argv)


        

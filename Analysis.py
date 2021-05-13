from project.models.Hotel import Hotel
from project.controllers.DataPreprocess import build_hotel_obj_data, build_hotel_review_data, calculate_universal_score
from project.controllers.QueryProcess import *
# from project.controllers.
import pickle
import time


data = build_hotel_obj_data('./Trip-Advisor-json/*.json')
with open('hotel_list.pkl', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

data2 = build_hotel_review_data('./Trip-Advisor-json/*.json')

with open('hotel_reviews.pkl', 'wb') as handle:
    pickle.dump(data2, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('DONE!')

with open('hotel_list.pkl', 'rb') as handle:
    hotel_obj = pickle.load(handle)
h_d = {}
for obj in hotel_obj:
    if obj.name not in h_d:
        h_d[obj.name] = obj
hotel_obj = list(h_d.values())

with open('hotel_reviews.pkl', 'rb') as handle:
    review_data = pickle.load(handle)

###############################################################################
#       CALCULATING TF -- TAKES A LONG TIME TO RUN!!!                         #
###############################################################################
tf_data = build_tf_data(hotel_obj,review_data)                
with open('review_tf.pkl', 'wb') as handle:
    pickle.dump(tf_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
###############################################################################
with open('review_tf.pkl', 'rb') as handle:
    tf_dict = pickle.load(handle)

print('Done!!')
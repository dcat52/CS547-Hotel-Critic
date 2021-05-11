from project.models.Hotel import Hotel
from project.controllers.DataPreprocess import build_hotel_obj_data, build_hotel_review_data, calculate_universal_score
from project.controllers.QueryProcess import *
# from project.controllers.
import pickle
import time


# data = build_hotel_obj_data('./Trip-Advisor-json/*.json')
# print(len(data))
# print(data[0])

# with open('hotel_list.pkl', 'wb') as handle:
#     pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# data2 = build_hotel_review_data('./Trip-Advisor-json/*.json')


# print(data2['72572'])

# with open('hotel_reviews.pkl', 'wb') as handle:
#     pickle.dump(data2, handle, protocol=pickle.HIGHEST_PROTOCOL)

# print('DONE!')
# print('DONE!')

with open('hotel_list.pkl', 'rb') as handle:
    hotel_obj = pickle.load(handle)
with open('hotel_reviews.pkl', 'rb') as handle:
    review_data = pickle.load(handle)

###############################################################################
#       CALCULATING TF -- TAKES A LONG TIME TO RUN!!!                         #
###############################################################################
# tf_data = build_tf_data(hotel_obj,review_data)                
# with open('review_tf.pkl', 'wb') as handle:
#     pickle.dump(tf_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
###############################################################################
with open('review_tf.pkl', 'rb') as handle:
    tf_dict = pickle.load(handle)

location = 'worcester'
text = 'clean hotel'
matched_hotels = parse_location(hotel_obj, location)
for obj in matched_hotels:
    score = cal_final_score(obj, text, tf_dict)
    print(obj.name, score)
# idf_data = build_idf_data(hotel_obj, tf_dict)
# with open('review_idf.pkl', 'wb') as handle:
#     pickle.dump(idf_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open('review_idf.pkl', 'rb') as handle:
#     idf_data = pickle.load(handle)
# print(idf_data['is'])

# tf_data = {}
# for hid in data2:
#     tf_data[hid] = Counter(data2[hid])

    
# for i in range(len(app.data)):
#     app.data[i].comment = None

# with open('data2.pkl', 'wb') as handle:
#     pickle.dump(app.data, handle, protocol=pickle.HIGHEST_PROTOCOL)
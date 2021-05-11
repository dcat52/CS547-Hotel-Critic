from project.models.Hotel import Hotel
from project.controllers.DataPreprocess import build_hotel_obj_data, build_hotel_review_data
from project.controllers.QueryProcess import *

import pickle
import time


data = build_hotel_obj_data('./Trip-Advisor-json/*.json')
print(len(data))
print(data[0])

with open('hotel_list.pkl', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

data2 = build_hotel_review_data('./Trip-Advisor-json/*.json')
print(len(data2))
# print(data2)
# print(data2['72572'])

with open('hotel_reviews.pkl', 'wb') as handle:
    pickle.dump(data2, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('DONE!')
print('DONE!')

# with open('hotel_list.pkl', 'rb') as handle:
#     hotel_obj = pickle.load(handle)
# with open('hotel_reviews.pkl', 'rb') as handle:
#     review_data = pickle.load(handle)
# print(hotel_obj[0].id)
# # print(data2.keys())

# tf_data = build_tf_data(hotel_obj,review_data)
# print(tf_data.keys())
# tf_data = {}
# for hid in data2:
#     tf_data[hid] = Counter(data2[hid])

    
# for i in range(len(app.data)):
#     app.data[i].comment = None

# with open('data2.pkl', 'wb') as handle:
#     pickle.dump(app.data, handle, protocol=pickle.HIGHEST_PROTOCOL)
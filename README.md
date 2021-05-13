# About Hotel Critic
Hotel Critic is a **search engine** for hotels. It allows users to search for hotels by typing their preferences in a completely free text way. 

There are 2 input fields
- **Search Query** - a field to input free text search query 
> E.g. clean and fast internet with a pool, good service and cheap
- **Location Filter** - a field to input location
> E.g. Boston, Paris

## Website 
Our search engine [Hotel Critic](https://hotelcritic.azurewebsites.net/) is hosted **live** on Azure. Please feel free to visit our website and give it try!

# Project Overview
Our project focuses on the hotel business, and aims to utilize and extract the data from hotel reviews to provide relevant free-text search results to the user. We intend to build a search engine that will analyze the customer reviews of hotels from a particular data set, filter the data by metrics such as location, price, cleanliness, service etc., rank the data according to the user's keywords, and output a list of ranked relevant results. We intend to implement a tool that can provide results of accuracy and quality for users.

## Data
Currently we are using a [TripAdvisor Dataset](http://times.cs.uiuc.edu/~wang296/Data/) that was crawled by DAIS Lab from University of Illinois for other research purpose. 
> Note: The version we used is the **JSON** version.
##  How to Run Our Code
Our code is written in **Python 3**. Please check your python version on your terminal by typing
```
python3 --version
```
### What to Install
```
pip -r requirements.txt
```
### Get Data
```
python3 Analysis.py
```
### Run the code
After finishing all the previous steps, you should have **review_tf.pkl**, **hotel_list.pkl** and **hotel_reviews.pkl** in your local folder
```
python3 server.py
```
Then **copy** the temporary url to a browser to use it **locally**

# Developer
**Davis Catherman** dscatherman@wpi.edu
**Shijing Yang** syang@wpi.edu
**Shine Lin Thant** slinnthant@wpi.edu

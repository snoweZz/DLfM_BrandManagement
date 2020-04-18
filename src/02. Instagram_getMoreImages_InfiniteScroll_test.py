# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 20:02:36 2020

@author: lsamsi
"""


import os
from random import choice
import json
import pandas as pd
import numpy as np
import csv
# load modules 
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from keras.preprocessing.image import load_img, img_to_array
import shutil 
# to install
import requests
from bs4 import BeautifulSoup


# TODO: without saving on PC, display image in IDE 




#%%

# pip install git+https://git@github.com/ping/instagram_private_api.git@1.6.0
from instagram_private_api import Client, ClientCompatPatch

user_name = 'chenpeling@hotmail.com'
password = 'Instagram2020'
USERNAME = 'nestle' # official nestle page: 'nestle'
HASHTAG = 'longines'
LIMIT_IMAGE_COUNT = 50 # 1st: 0, 2nd: 36, 3rd: 72 stops, at the first step over 50 


# initialize client 
api = Client(user_name, password)



#%%
########### HASHTAG ###################

# all images urls 
all_hash_image_posts_urls = []

next_max_id = None
while (api.feed_tag(HASHTAG, api.generate_uuid())["more_available"] == True) and (len([item for sublist in all_hash_image_posts_urls for item in sublist]) <= LIMIT_IMAGE_COUNT): 
    if next_max_id == None: 
        #Gets the first 12 posts
        posts = api.feed_tag(HASHTAG, api.generate_uuid())
        len(posts['items'])
        image_urls = []
        for i in range(len(posts['items'])): 
            try: 
                url = posts['items'][i]['image_versions2']['candidates'][0]['url'] # some posts do not have 'image_version2', they are overlooked in that case
                image_urls.append(url)
            except: 
                pass 
        # Extract the value *next_max_id* from the above response, this is needed to load the next 12 posts
        next_max_id = posts["next_max_id"] 
        all_hash_image_posts_urls.append(image_urls)
    else: 
        next_page_posts = api.feed_tag(HASHTAG, api.generate_uuid())
        len(next_page_posts['items'])
        # get image urls 
        next_image_urls = []
        for i in range(len(next_page_posts['items'])):
            try: 
                url = next_page_posts['items'][i]['image_versions2']['candidates'][0]['url']
                next_image_urls.append(url)
            except: 
                pass
        # Extract the value *next_max_id*
        next_max_id = next_page_posts["next_max_id"] 
        all_hash_image_posts_urls.append(next_image_urls)

else:        
    flat_hash_image_posts_urls = [item for sublist in all_hash_image_posts_urls for item in sublist]
    print(f"A total of {len(flat_hash_image_posts_urls)} image post urls were retrieved from the Instagram page.")
    

#%%
########### USERNAME ###################

# all images urls 
all_image_posts_urls = []

next_max_id = None
while (api.username_feed(USERNAME, max_id = next_max_id)["more_available"] == True)  and (len([item for sublist in all_image_posts_urls for item in sublist]) <= LIMIT_IMAGE_COUNT): 
    if next_max_id == None: 
        #Gets the first 12 posts
        posts = api.username_feed(USERNAME)
        len(posts['items'])
        image_urls = []
        for i in range(len(posts['items'])): 
            url = posts['items'][i]['image_versions2']['candidates'][0]['url']
            image_urls.append(url)
        # Extract the value *next_max_id* from the above response, this is needed to load the next 12 posts
        next_max_id = posts["next_max_id"] 
        all_image_posts_urls.append(image_urls)
    else: 
        next_page_posts = api.username_feed(USERNAME, max_id = next_max_id)
        len(next_page_posts['items'])
        # get image urls 
        next_image_urls = []
        for i in range(len(next_page_posts['items'])):
            try: 
                url = next_page_posts['items'][i]['image_versions2']['candidates'][0]['url']
                next_image_urls.append(url)
            except: 
                pass
        # Extract the value *next_max_id*
        next_max_id = next_page_posts["next_max_id"] 
        all_image_posts_urls.append(next_image_urls)
        
else: 
    flat_image_posts_urls = [item for sublist in all_image_posts_urls for item in sublist]
    print(f"A total of {len(flat_image_posts_urls)} image post urls were retrieved from the Instagram page.")



### Request Errors: 
# ClientConnectionError: URLError <urlopen error timed out>
        
# if Timeout: spyder/plugins/ipythonconsole/comms/kernelcomm.py 
# timeout = 10

#%%

#Saving cookies
# cookies = api.cookie_jar.dump()
# with open("cookies.pkl", "wb") as save_cookies:
#     save_cookies.write(cookies)

# #Loading cookies
# with open("cookies.pkl", "rb") as read_cookies:
#     cookies = read_cookies.read()

# #Pass cookies to Client to resume session
# api = Client(user_name, password, cookie = cookies)





#%%

# set directory 
directory= r"C:\Users\lsamsi\Documents\GitHub\DLfM_BrandManagement\data\instagram_images\football"
os.chdir(directory)

          
# save HASHTAG images to PC 
for i in range(len(flat_hash_image_posts_urls)):
    r = requests.get(flat_hash_image_posts_urls[i], stream=True)
    with open(f"{i}_"+flat_hash_image_posts_urls[i][-34:]+".png", 'wb') as f:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        # Copy the response stream raw data to local image file.
        shutil.copyfileobj(r.raw, f)
        # Remove the image url response object.
        del r
        
 #%%       

# save USERNAME images to PC 
for i in range(len(flat_image_posts_urls)):
    for j in range(len(flat_image_posts_urls[i])):
        r = requests.get(flat_image_posts_urls[i][j], stream=True)
        with open(f"{i}_"+flat_image_posts_urls[i][j][-34:]+".png", 'wb') as f:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            # Copy the response stream raw data to local image file.
            shutil.copyfileobj(r.raw, f)
            # Remove the image url response object.
            del r


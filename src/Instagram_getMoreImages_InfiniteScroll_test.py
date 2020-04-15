# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 20:02:36 2020

@author: lsamsi
"""


import os
from random import choice
import json
import pandas as pd
import csv
# load modules 
import imageio
import json
import numpy as np
# to install
import requests
from bs4 import BeautifulSoup

# TODO: for inofficial instagram page 
# TODO: without saving on PC, display image in IDE 

# set directory 
directory= r"C:\Users\lsamsi\Documents\GitHub\DLfM_BrandManagement\data\instagram_images\nestle"
os.chdir(directory)


#%%

# pip install git+https://git@github.com/ping/instagram_private_api.git@1.6.0
from instagram_private_api import Client, ClientCompatPatch

user_name = 'chenpeling@hotmail.com'
password = 'Instagram2020'
username_to_scrape = 'nestle' # official nestle page: 'nestle'
url = "https://www.instagram.com/nestle/"


# initialize client 
api = Client(user_name, password)

# all images urls 
all_image_posts_urls = []
next_max_id = None
while api.username_feed(username_to_scrape, max_id = next_max_id)["more_available"] == True: 
    if next_max_id == None: 
        #Gets the first 12 posts
        posts = api.username_feed(username_to_scrape)
        len(posts['items'])
        image_urls = []
        for i in range(len(posts['items'])): 
            url = posts['items'][i]['image_versions2']['candidates'][0]['url']
            image_urls.append(url)
        # Extract the value *next_max_id* from the above response, this is needed to load the next 12 posts
        next_max_id = posts["next_max_id"] 
        all_image_posts_urls.append(image_urls)
    else: 
        next_page_posts = api.username_feed(username_to_scrape, max_id = next_max_id)
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
        

flat_image_posts_urls = [item for sublist in all_image_posts_urls for item in sublist]
print(f"A total of {len(flat_image_posts_urls)} image post urls were retrieved from the Instagram page.")
# ClientConnectionError: URLError <urlopen error timed out>
        
# if Timeout: spyder/plugins/ipythonconsole/comms/kernelcomm.py 
# timeout = 10

#%%

#Saving cookies
cookies = api.cookie_jar.dump()
with open("cookies.pkl", "wb") as save_cookies:
    save_cookies.write(cookies)

#Loading cookies
with open("cookies.pkl", "rb") as read_cookies:
    cookies = read_cookies.read()

#Pass cookies to Client to resume session
api = Client(user_name, password, cookie = cookies)




#%%
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import shutil 


# save images to PC 
for i in range(len(all_image_posts_urls)):
    for j in range(len(all_image_posts_urls[i])):
        r = requests.get(all_image_posts_urls[i][j], stream=True)
        with open(f"{i}_"+all_image_posts_urls[i][j][-34:]+".png", 'wb') as f:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            # Copy the response stream raw data to local image file.
            shutil.copyfileobj(r.raw, f)
            # Remove the image url response object.
            del r


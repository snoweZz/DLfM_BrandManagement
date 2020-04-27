#!/usr/bin/env python
# coding: utf-8

##########################################
# # Image Retrieval From Instagram   # #
##########################################
#
# 
# **Goal:** collect image data from instagram and then preprocess it, extract information (image files) from a user's Instagram profile
# 
# **Constraints:** the user has no way of setting the image size (in KB), the resolution (1080x1080) of the images found on Instagram. The images are extracted from the Instagram page in raw form.  

# **Important Note:** *Remember to respect user’s rights when you download copyrighted content. Do not use images/videos from Instagram for commercial intent.*

# ### 1. Import dependencies
# 
# Install non-standard libraries: requests, BeautifulSoup 

# In[1]:


import os
from random import choice
import json
import pandas as pd
import csv

# to install
import requests
from bs4 import BeautifulSoup


# ### 2. Build InstagramScraper class
# based on: https://edmundmartin.com/scraping-instagram-with-python/

# Switching user agents is often a best practice when web scraping and can help you avoid detection. Should the caller of our class have provided their own list of user agents we take a random agent from the provided list.  Otherwise we will return our default user agent.

# Define a class called InstagramScraper: 

# In[2]:


# url header for requests.get()
headers={'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
         ,  'content-type': 'application/json'
         , 'accept-encoding': 'gzip, deflate, br'
         , 'cache-control': 'no-cache'
         , 'accept' : '*/*'
         , 'accept-language' : 'de-DE, de; q=0.9,en-US; q=0.8,en;q=0.7'
         #, 'referer' : url
         , 'connection' : 'keep-alive'
         , 'cookie' : 'ig_cb=1; ig_did=DA66C494-9DFE-48F6-BA63-66F11DF8EC03; csrftoken=ukE8jYSjQxVs1YGPYddEkAXsN6WZ4Qmw; mid=XoChrAALAAG78Upva7Ld0TAzeTtm; rur=ASH; urlgen="{\"2a04:ee41:4:95:91f9:b9d4:8aab:41c\": 15796\054 \"213.55.241.7\": 15796\054 \"2a04:ee41:4:95:60ae:def3:2fd7:3633\": 15796}:1jIpww:PTjjrSzpjC6dWww8-AVOnfdQAFA"'
        }
_user_agents = [
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]


# In[3]:


class InstagramScraper:

    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __request_url(self, url):
        """Our second helper method is simply a wrapper around requests. 
        We pass in a URL and try to make a request using the provided user agent and proxy. 
        If we are unable to make the request or Instagram responds with a non-200 status code we simply re-raise the error. 
        If everything goes fine, we return the page in questions HTML."""
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy, 'https': self.proxy})
            #response = requests.get(url, headers=headers, proxies={'http': self.proxy, 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException('Internet connection failed.')
        else:
            return response.text


    @staticmethod
    def extract_json_data(html):
        """Instagram serve’s all the of information regarding a user in the form of JavaScript object. 
        This means that we can extract all of a users profile information and their recent posts by just 
        making a HTML request to their profile page. We simply need to turn this JavaScript object into 
        JSON, which is very easy to do."""
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def profile_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                #print('key:', key, '-value:', value)
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
                    elif value:
                        results[key] = value
        return results

    
    def hash_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['TagPage'][0]['graphql']['hashtag']
         
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                #print('metrics:', metrics)
                if key != 'edge_hashtag_to_media' and key != 'edge_hashtag_to_top_posts' and key != 'profile_pic_url':
                    results[key] = value
                    if value and isinstance(value, dict):
                        try: 
                            value = value['count']            
                            results[key] = value
                        except: 
                            results[key] = value
                        try: 
                            sigma = []
                            for i in range(0,5): 
                                #print(i)
                                value = value['edges'][i]['node']['name']  
                                #print(i)
                            sigma.append(value)
                            print(len(value['edges']['node']))
                            
                            #results[key] = sigma
                        except: 
                            results[key] = value 
                    elif value:
                        results[key] = value
        return results
    
    def profile_page_posts(self, profile_url):
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"]
            #pprint(metrics)
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                #if node and isinstance(node, dict): #this line only gets most recent post out
                results.append(node)
        return results
    
    def hashtag_page_posts(self, hashtag_url):
        results = []
        try:
            response = self.__request_url(hashtag_url)
            json_data = self.extract_json_data(response)
            #pprint(json_data)
            metrics = json_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']["edges"]
            #pprint(metrics)
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                #if node and isinstance(node, dict): #this line only gets most recent post out
                results.append(node)
        return results


# ### 3.1 Load URLS of Brand Names Data
# 
# Specify instragram USERNAME profile whose page you want to scrape. Get a dictionary with all information (image, comments, etc.) from that Instagram profile.

# In[4]:


# to specify
try: 
    directory= r'C:\Users\Anonym\Documents\GitHub\DLfM_BrandManagement\data\instagram_urls'
    os.chdir(directory)
except: 
    directory = r'C:\Users\lsamsi\Documents\GitHub\DLfM_BrandManagement\data\instagram_urls'
    os.chdir(directory)



# ### 3.2 Specify Instagram page(s)
# 
# Specify instragram USERNAME profile whose page you want to scrape. Get a dictionary with all information (image, comments, etc.) from that Instagram profile. 

# #### Convert unofficial hashtag to official user-profile name 
# 
# For 'cailler' the '#cailler' user-input will get results on Instagram. The officiel Instagram of cailler might differ, however. 
# The official brandname on Instagram is 'cailler-suisse'. Thus, we need a dataframe to get out the corresponding official name given the unofficial name. 
# 
# This is the reason why **we can only have brands that are listed in this dataframe** and **no other brands**.

# In[54]:


# set directory 
#import os
#directory= r"C:\Users\Anonym\Documents\GitHub\DLfM_BrandManagement\data\instagram_urls"
#os.chdir(directory)


# In[5]:


# load dataframe 
import pandas as pd 

convert = pd.read_csv('hashToOfficialName.csv')


# In[6]:


convert.head()


# In[57]:


# pages that have access denial because of age limit
# are you 18/21 or over? 
#urls.remove('https://www.instagram.com/bacardiusa/?hl=en')


# In[13]:


# items to be removed from conversion dataframe 
agelimited_brands = ['bacardiusa', 'budlight', 'budweiser', 'coorslight', 'corona', 'greygoose', 'jackdaniels_us', 'korbel_1882'] 

convert = convert[~(convert.firm_account.isin(agelimited_brands))]
convert.head()


# In[8]:


def hashToOfficial(hashing): 
    username = convert.loc[convert['instagram_hashtag'] == hashing, 'firm_account'].iloc[0]
    return username



# #### Keyword input

# In[9]:


brands_on_display = convert['instagram_hashtag'].tolist()
brands_on_display = ', '.join(brands_on_display)


# In[10]:


print('Choose from these brandnames to get a brand management analysis:', brands_on_display)
keyword = input('Which brandname do you want to analyze?')
# 'sanpellegrino'


# #### Hashtag Page
# 
# If you want to open a hashtag page (instead of a user profile): 

# In[11]:


# for one brand only 

# to specify user_input
hashtag = keyword 
hash_url = 'https://www.instagram.com/explore/tags/'+hashtag


# #### User-profile Page
# 
# If you want to scrape a user-profile page, specify the username as:

# In[14]:


# for one firm only 

# to specify user_input
username= hashToOfficial(hashtag)
url = 'https://www.instagram.com/'+username+'/?hl=en'


# ### 3. Get information from Instagram page(s) [optional]
# 
# Now that the url of the Instagram page is defined, it will extract out all the posts or meta-information from the website usinge the InstagramScraper class. 
# 
# Get meta-information metrics by using a class method. 


# In[16]:


# get posts (images) from single profile page 

from pprint import pprint

k = InstagramScraper()
results = k.profile_page_posts(url)

print('Instagram page: ', url)
print('Posts on Instagram profile page: ', len(results))
print('Second image url on instagram profile: ', results[1]['display_url'])


# #### Hashtag Page
# 
# Get all posts on an Instagram **hashtag page** that are visible on the landing page. 

# In[17]:


# get posts (images) from a hashtag page 
from pprint import pprint

k = InstagramScraper()
hash_results = k.hashtag_page_posts(hash_url)

print('Instagram page: ', url)
print('Posts on Instagram hashtag page: ', len(hash_results))
print('Second image url on instagram hashtag: ', hash_results[1]['display_url'])


# ### 5. Save images into folders
# 
# Save images from list of dict: Use requests library to download images from the ‘display_url’ in pandas ‘result’ data frame and store them with respective shortcode as file name.
# 
# Specify the directory for storing the images. 

# In[19]:


# load modules
import os
import requests
import shutil


# Some functions...

# In[20]:


def set_root_path_images(): 
    
    # to specify
    try: 
        directory= r"C:\Users\Anonym\Documents\GitHub\DLfM_BrandManagement\data"
        os.chdir(directory)
    except: 
        directory= r"C:\Users\lsamsi\Documents\GitHub\DLfM_BrandManagement\data"
        os.chdir(directory)
    folder = 'instagram_images' #image root folder, all subfolders' name are firmnames

    os.chdir(directory)

    try: 
        os.mkdir(folder)
    except: 
        pass

    path = os.path.join(directory, folder)
    os.chdir(path)
    return path 


# In[21]:


def build_folders_images(account, folder, path): 
        try: 
            os.mkdir(os.path.join(path, account))
        except: 
            pass
        
        # set directory 
        directory = os.path.join(path, account)
        os.chdir(directory)   
        try: 
            os.mkdir(folder)
            print('new folder created for: ', account)
        except: 
            pass
        path = os.path.join(directory, folder)
        os.chdir(path)
        return path 


# In[22]:


# load modules 
import imageio
import json
import numpy as np

# set directory 
path = set_root_path_images()


# In[23]:


# create folders
build_folders_images(hashtag, 'official', path)
print('Directory set to: ', os.getcwd())


# In[29]:


#https://gist.github.com/abhaymise/b011f9d68456f1d87561d71af2f7fd6a

# save images to PC 
for i in range(len(results)):
    r = requests.get(results[i]['display_url'], stream=True)
    with open(f"{i}_"+results[i]['shortcode']+".png", 'wb') as f:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        # Copy the response stream raw data to local image file.
        shutil.copyfileobj(r.raw, f)
        # Remove the image url response object.
        del r
        


# In[25]:


# specify image dimension
IMG_WIDTH=300
IMG_HEIGHT=300
IMG_DIM = (IMG_WIDTH, IMG_HEIGHT)


# In[26]:


# load modules 
from io import BytesIO
import base64
from PIL import Image
from keras.preprocessing.image import load_img, img_to_array

# list of images as np.arrays 
images_lst = []
#np.array([0])
for i in range(len(results)):

    # load image 
    train_imgs = img_to_array(load_img(f"{i}_"+results[i]['shortcode']+".png", target_size=IMG_DIM))
    train_imgs = np.array(train_imgs)
    images_lst.append(train_imgs)


# In[27]:


# all images as numpy array (for feeding as X_test)
images_np = np.stack(images_lst, axis=0)
print(images_np.shape)


# In[28]:


# set directory 
path = set_root_path_images()

np.save(f'{hashtag}_official_npimgs.npy', images_np)


# #### Hashtag page

# In[30]:


# load modules 
import imageio
import json
import numpy as np

# set directory 
path = set_root_path_images()


# In[31]:


# create folders
build_folders_images(hashtag, 'unofficial', path)
print('Directory set to: ', os.getcwd())


# In[32]:


#https://gist.github.com/abhaymise/b011f9d68456f1d87561d71af2f7fd6a

# save images to PC
for i in range(len(hash_results)):
    r = requests.get(hash_results[i]['display_url'], stream=True)
    with open(f"{i}_"+hash_results[i]['shortcode']+".png", 'wb') as f:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        # Copy the response stream raw data to local image file.
        shutil.copyfileobj(r.raw, f)
        # Remove the image url response object.
        del r


# In[33]:


# specify image dimension
IMG_WIDTH=300
IMG_HEIGHT=300
IMG_DIM = (IMG_WIDTH, IMG_HEIGHT)


# In[34]:


# load modules 
from io import BytesIO
import base64
from PIL import Image
from keras.preprocessing.image import load_img, img_to_array

# list of images as np.arrays 
hash_images_lst = []
for i in range(len(hash_results)):
    # load image 
    byteImg = Image.open(f"{i}_"+hash_results[i]['shortcode']+".png")
    # load image 
    train_imgs2 = img_to_array(load_img(f"{i}_"+hash_results[i]['shortcode']+".png", target_size=IMG_DIM))
    train_imgs2 = np.array(train_imgs2)
    hash_images_lst.append(train_imgs2)


# In[35]:


# all images as numpy array (for feeding as X_test)
hash_images_np = np.stack(hash_images_lst, axis=0)
print(hash_images_np.shape)


# In[36]:


# set directory 
path = set_root_path_images()

np.save(f'{hashtag}_unofficial_npimgs.npy', hash_images_np)


# In[ ]:





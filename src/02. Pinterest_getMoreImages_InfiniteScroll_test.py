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


# set directory 
directory= r"C:\Users\lsamsi\Documents\GitHub\DLfM_BrandManagement\data\pinterest_images"
os.chdir(directory)


#%%

# pip install pinterest-api
import pinterest

# How to Get OAuth Access Token for Pinterest?
# First, register for an app to get your app_id and set up a redirect URI:
# https://developers.pinterest.com/manage/
# name: pinterestanalytics4brands

# Then, find your client secret under Signature Tester:
# https://developers.pinterest.com/tools/signature/
# Bring the user to the OAuth dialog like this:
# https://www.pinterest.com/oauth/?consumer_id=[client_id]&response_type=[code_or_token]&scope=[list_of_scopes]

user_name = 'chenpeling@hotmail.com'
password = 'Instagram2020'
username_to_scrape = 'nestle' # official nestle page: 'nestle'
url = "https://www.instagram.com/nestle/"



# Generate OAuth2 authorization link
link = pinterest.oauth2.authorization_url(app_id, redirect_uri)


# Initialize API by passing OAuth2 token
api = pinterest.Pinterest(token="ApFF9WBrjug_xhJPsETri2jp9pxgFVQfZNayykxFOjJQhWAw")


# Fetch authenticated user's data
api.me()

# Fetch authenticated user's boards
api.boards()

# Create board
api.board().create("Halloween", description="Fun Costumes")

# Fetch board
api.board("695665542379607495").fetch()
api.board("username/halloween").fetch()

# Fetch pins on board
api.board("username/halloween").pins()

# Edit board
api.board("username/halloween").edit(new_name="Costumes", new_description="Halloween Costume Ideas")

# Delete board
api.board("username/halloween").delete()

# Fetch board suggestions
api.suggest_boards(pin=162129655315312286)

# Fetch authenticated user's pins
api.pins()

# Create a pin
api.pin().create(board, note, link, image_url=image_url)

# Fetch a pin
api.pin(162129655315312286).fetch()

# Edit a pin
api.pin(162129655315312286).edit(board, note, link)

# Delete a pin
api.pin(162129655315312286).delete()

# Search boards (Optional cursor)
api.search_boards(query, cursor=None)

# Search pins (Optional cursor)
api.search_pins(query, cursor=None)

# Follow a board
api.follow_board(board)

# Follow a user
api.follow_user(username)

# Return the users who follow the authenticated user
api.followers(cursor=None)

# Return the boards that the authenticated user follows
api.following_boards(cursor=None)

# Return the topics the authenticated user follows
api.following_interests(cursor=None)

# Return the users the authenticated user follows
api.following_users(cursor=None)

# Unfollow board
api.unfollow_board(board)

# Make authenticated user unfollow user
api.unfollow_user(username)

# Fetch another user's info
api.user(username)

# Fetch board sections
api.board("695665542379586148").sections()

# Create board section
api.board("695665542379586148").section("Section Title").create()

# Delete board section
api.board("695665542379586148").section("4989415010584246390").delete()

# Fetch pins in board section
api.board("695665542379586148").section("4989343507360527350").pins()
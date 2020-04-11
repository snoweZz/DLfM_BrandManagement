from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from src.utils import instagram_scraper
from src.utils import image_preprocessing
from src.utils import label_encoding
import requests
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
model = load_model('model/demo_model.h5')

def data_collection(brandname):
    url = 'https://www.instagram.com/'+brandname+'/?hl=en'
    scraper = instagram_scraper.InstagramScraper()
    official_images = scraper.profile_page_posts(url)
    #print('Instagram page: ', url)
    #print('Posts on Instagram profile page: ', len(official_images))
    #print('Second image url on instagram profile: ', official_images[1]['display_url'])
    return official_images


def data_preprocessing(official_images):
    preprocessed_data = image_preprocessing.preprocessing(official_images)
    return preprocessed_data


def make_prediction(preprocessed_data):
    print('model type: {}'.format(type(model)))
    print('model summary: {}'.format(model.summary()))
    X_test = preprocessed_data
    print('X_test shape: {}'.format(X_test.shape))
    print('X_test type: {}'.format(type(X_test)))
    y_pred = model.predict(X_test) # Crashes here
    print('y_pred: {}'.format(y_pred))
    # convert from encoded label to label name
    label_encoder = LabelEncoder()
    y_pred = label_encoding.probabilty_to_classencoding(y_pred)
    y_pred = label_encoding.binary_class_to_label(y_pred)
    # encoded label
    y_pred_lst = y_pred.tolist()
    # map back to original label name
    code2label = {0: 'fun', 1: 'glamarous', 2: 'healthy', 3: 'negative'}
    y_pred_lbnm = map(code2label.get, y_pred_lst)
    y_pred_lbnm = list(y_pred_lbnm)
    prediction = pd.Series(y_pred_lbnm).value_counts()
    return prediction


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        brandname = request.form["brandname"]
        return redirect(url_for("predict", brandname=brandname))
    else:
        return render_template("index.html")


@app.route("/predict/<brandname>", methods=["POST", "GET"])
def predict(brandname):
    official_images = data_collection(brandname)
    preprocessed_data = data_preprocessing(official_images)
    prediction = make_prediction(preprocessed_data)
    return render_template("predict.html", prediction=prediction)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
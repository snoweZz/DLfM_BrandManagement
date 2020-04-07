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
# small comment for merge
app = Flask(__name__)
model = load_model('model/demo_model.h5')

def data_collection(user_input):
    return user_input


def data_preprocessing(instagram_images):
    return instagram_images


def make_prediction(preprocessed_data):
    return preprocessed_data


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        brandname = request.form["brandname"]
        return redirect(url_for("predict", brandname=brandname))
    else:
        return render_template("index.html")


@app.route("/predict/<brandname>", methods=["POST", "GET"])
def predict(brandname):
    instagram_images = data_collection(brandname)
    preprocessed_data = data_preprocessing(instagram_images)
    prediction = make_prediction(preprocessed_data)
    return render_template("predict.html", prediction=prediction)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
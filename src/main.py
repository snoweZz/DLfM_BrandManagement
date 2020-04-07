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
model = load_model('./playground/demo_model.h5')

# script works but always returns the same number as prediction...
# TODO: figure out where the problem is and reconstruct the modelling process more carefully/systematically


def data_collection(id):
    dataset = pd.read_csv('playground/data/mobile-price-classification/test.csv')
    test_data = dataset.iloc[id-1, ]
    return test_data


def data_preprocessing(data):
    sc = StandardScaler()
    data = np.array(data)
    reshaped_data = data.reshape(1, -1)
    ppdata = sc.fit_transform(reshaped_data)
    return ppdata[:,1:]

def make_prediction(ppdata):
    ypred = model.predict(ppdata)
    return ypred


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        user_input = int(request.form["nm"])
        data = data_collection(user_input)
        #print(data)
        preprocessed_data = data_preprocessing(data)
        prediction = make_prediction(preprocessed_data)
        #brandname = data_preprocessing(user_input)
        return redirect(url_for("predict", bn=prediction))
    else:
        return render_template("index.html")


@app.route("/<bn>", methods=["POST", "GET"])
def predict(bn):
    return render_template("predict.html", brandname=bn)


if __name__ == "__main__":
    app.run(debug=True)


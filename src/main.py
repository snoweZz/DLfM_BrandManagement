from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import tensorflow as tf
from keras.models import load_model
from keras.backend import set_session
from src.utils import instagram_scraper
from src.utils import image_preprocessing
from src.utils import label_encoding
from src.utils import overall_class_label
from sklearn.preprocessing import LabelEncoder

global sess
global graph
sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)
num_attributes = 4
model = [[] for i in range(num_attributes)]
model[0] = load_model('./model/savemodels/glamorous_model.h5')
model[1] = load_model('./model/savemodels/rugged_model.h5')
model[2] = load_model('./model/savemodels/fun_model.h5')
model[3] = load_model('./model/savemodels/healthy_model.h5')


app = Flask(__name__)


def data_collection(official, unofficial):
    url_official = official
    url_unofficial = 'https://www.instagram.com/explore/tags/'+unofficial+''
    scraper = instagram_scraper.InstagramScraper()
    official_images = scraper.profile_page_posts(url_official)
    unofficial_images = scraper.hashtag_page_posts(url_unofficial)
    return official_images, unofficial_images


def data_preprocessing(official_images, unofficial_images):
    preprocessed_data_official = image_preprocessing.preprocessing(official_images)
    preprocessed_data_unofficial = image_preprocessing.preprocessing(unofficial_images)
    return preprocessed_data_official, preprocessed_data_unofficial


def make_prediction(preprocessed_data):
    X_test = preprocessed_data

    with graph.as_default():
        set_session(sess)
        y_pred = [[] for i in range(num_attributes)]
        for i in range(num_attributes):
            y_pred[i] = model[i].predict(X_test)
        y_pred_label = overall_class_label.give_ovr_class_label_output(y_pred)

    # convert from encoded label to label name
    # label_encoder = LabelEncoder() never used?
    # encoded label
    y_pred_lst = y_pred_label.tolist()
    # map back to original label name
    code2label = {0: 'glamorous', 1: 'rugged', 2: 'fun', 3: 'healthy'}
    y_pred_lbnm = map(code2label.get, y_pred_lst)
    y_pred_lbnm = list(y_pred_lbnm)
    #print(y_pred_lbnm)
    prediction = y_pred_lbnm#pd.Series(y_pred_lbnm).value_counts()
    total = len(prediction)
    return prediction, total


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        official = request.form["official"]
        unofficial = request.form["unofficial"]
        return redirect(url_for("predict", official=official, unofficial=unofficial))
    else:
        return render_template("index.html")


@app.route("/predict/", methods=["POST", "GET"])
def predict():
    official = request.args.get('official')
    unofficial = request.args.get('unofficial')
    official_images, unofficial_images = data_collection(official, unofficial)
    preprocessed_data_official, preprocessed_data_unofficial = data_preprocessing(official_images, unofficial_images)
    prediction_official, total_official = make_prediction(preprocessed_data_official)
    prediction_unofficial, total_unofficial = make_prediction(preprocessed_data_unofficial)
    return render_template("predict.html", prediction_official=prediction_official, total_official=total_official,
                           prediction_unofficial=prediction_unofficial, total_unofficial=total_unofficial)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
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

# sessions and default graphs are needed to make tensorflow work properly
global sess
global graph
sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)
num_attributes = 4
model = [[] for i in range(num_attributes)]
model[0] = load_model('../model/savemodels/glamorous_model.h5')
model[1] = load_model('../model/savemodels/rugged_model.h5')
model[2] = load_model('../model/savemodels/fun_model.h5')
model[3] = load_model('../model/savemodels/healthy_model.h5')


app = Flask(__name__)


# this function collects images from the user specified instagram page and hashtag respectively
# url_official is the official instagram page url of the brand to be analysed
# url_unofficial is the hashtag instagram page url we want to compare to the official page
def data_collection(official, unofficial):
    url_official = official
    url_unofficial = 'https://www.instagram.com/explore/tags/'+unofficial+''
    scraper = instagram_scraper.InstagramScraper()
    official_images = scraper.profile_page_posts(url_official)
    unofficial_images = scraper.hashtag_page_posts(url_unofficial)
    return official_images, unofficial_images


# this function reformats the collected images to make them usable as model input (X_test)
# the images are stored in python objects, that way the user does not have to download images on his/her computer
def data_preprocessing(official_images, unofficial_images):
    preprocessed_data_official = image_preprocessing.preprocessing(official_images)
    preprocessed_data_unofficial = image_preprocessing.preprocessing(unofficial_images)
    return preprocessed_data_official, preprocessed_data_unofficial


# this function takes the preprocessed images and feeds them into the pretrained models
# as output we get a list with the predicted label for each image
def make_prediction(preprocessed_data):
    X_test = preprocessed_data

    # tensorflow specifics to correctly use a pretrained model
    with graph.as_default():
        set_session(sess)
        y_pred = [[] for i in range(num_attributes)]
        for i in range(num_attributes):
            y_pred[i] = model[i].predict(X_test)
        y_pred_label = overall_class_label.give_ovr_class_label_output(y_pred)
    # encoded label
    y_pred_lst = y_pred_label.tolist()
    # map back to original label name
    code2label = {0: 'glamorous', 1: 'rugged', 2: 'fun', 3: 'healthy'}
    y_pred_lbnm = map(code2label.get, y_pred_lst)
    y_pred_lbnm = list(y_pred_lbnm)
    prediction = y_pred_lbnm
    total = len(prediction)
    return prediction, total


# the homepage the user sees when starting the application
@app.route("/", methods=["POST", "GET"])
def index():
    # once the user entered the data and clicked on 'Predict', the data is captured and redirected to the predict page
    if request.method == "POST":
        official = request.form["official"]
        unofficial = request.form["unofficial"]
        return redirect(url_for("predict", official=official, unofficial=unofficial))
    else:
        return render_template("index.html")


# the page the user gets redirected to after hitting the 'Predict' button on the homepage
@app.route("/predict/", methods=["POST", "GET"])
def predict():
    official = request.args.get('official')
    unofficial = request.args.get('unofficial')
    official_images, unofficial_images = data_collection(official, unofficial)
    preprocessed_data_official, preprocessed_data_unofficial = data_preprocessing(official_images, unofficial_images)
    prediction_official, total_official = make_prediction(preprocessed_data_official)
    prediction_unofficial, total_unofficial = make_prediction(preprocessed_data_unofficial)

    # generate the numbers to be displayed in the analysis table
    # for official:
    fun_official = prediction_official.count('fun')
    glamorous_official = prediction_official.count('glamorous')
    healthy_official = prediction_official.count('healthy')
    rugged_official = prediction_official.count('rugged')
    # for unofficial:
    fun_unofficial = prediction_unofficial.count('fun')
    glamorous_unofficial = prediction_unofficial.count('glamorous')
    healthy_unofficial = prediction_unofficial.count('healthy')
    rugged_unofficial = prediction_unofficial.count('rugged')
    # for relative table:
    fun_official_rel = round(fun_official/total_official*100)
    fun_unofficial_rel = round(fun_unofficial/total_unofficial*100)
    glamorous_official_rel = round(glamorous_official / total_official*100)
    glamorous_unofficial_rel = round(glamorous_unofficial / total_unofficial*100)
    healthy_official_rel = round(healthy_official / total_official*100)
    healthy_unofficial_rel = round(healthy_unofficial / total_unofficial*100)
    rugged_official_rel = round(rugged_official / total_official*100)
    rugged_unofficial_rel = round(rugged_unofficial / total_unofficial*100)

    return render_template("predict.html", fo=fun_official, fu=fun_unofficial, fo_rel=fun_official_rel, fu_rel=fun_unofficial_rel,
                           go=glamorous_official, gu=glamorous_unofficial, go_rel=glamorous_official_rel, gu_rel=glamorous_unofficial_rel,
                           ho=healthy_official, hu=healthy_unofficial, ho_rel=healthy_official_rel, hu_rel=healthy_unofficial_rel,
                           ro=rugged_official, ru=rugged_unofficial, ro_rel=rugged_official_rel, ru_rel=rugged_unofficial_rel,
                           to=total_official, tu=total_unofficial, unofficial=unofficial)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
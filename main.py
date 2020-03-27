from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    res = 'Predict'
    return render_template("index.html", res=res)


if __name__ == "__main__":
    app.run(debug=True)


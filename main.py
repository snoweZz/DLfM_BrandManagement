from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        brandname = request.form["brandname"]
        return render_template("index.html", brandname=brandname)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)


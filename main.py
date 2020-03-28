from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        brandname = request.form["nm"]
        return redirect(url_for("predict", bn=brandname))
    else:
        return render_template("index.html")


@app.route("/<bn>", methods=["POST", "GET"])
def predict(bn):
    return render_template("predict.html", brandname=bn)


if __name__ == "__main__":
    app.run(debug=True)


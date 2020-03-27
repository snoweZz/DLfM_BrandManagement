from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    a = 3
    b = 5
    res = a+b
    return render_template("index.html", res=res)


if __name__ == "__main__":
    app.run(debug=True)


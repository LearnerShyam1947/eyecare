from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/predict")
def predict():
    return render_template("predict.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

from Api import api
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)

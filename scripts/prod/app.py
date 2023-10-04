from flask import Flask, jsonify
import pickle

app = Flask(__name__)

@app.route("/")
def hello():
    return("Hello from Flask!")

@app.route("/predict/<int:feature1>/<int:feature2>/<int:feature3>")
def predict(feature1, feature2, feature3):
    with open("./models/model.pkl", "rb") as fd:
        clf = pickle.load(fd)
    prediction = int(clf.predict([[feature1, feature2, feature3]])[0])
    return(jsonify({"house_price": prediction}))

if __name__=="__main__":
    app.run(host="0.0.0.0", port=55555)
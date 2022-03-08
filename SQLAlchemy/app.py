from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def home():
    return "The following routes are currently available:\n None"

@app.route("/api/v1.0/precipitation")
def precipitation():
    return "A JSON rep of a precipitation dictionary"

@app.route("/api/v1.0/stations")
def stations():
    return "a JSON list of stations from the dataset"

@app.route("/api/v1.0/tobs")
def tobs():
    return "a JSON list of temperature observations"

if __name__ == "__main__":
app.run(debug=True)

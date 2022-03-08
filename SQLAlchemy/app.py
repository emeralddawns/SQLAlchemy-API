import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime
import time

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc

from flask import Flask, jsonify


# create engine to hawaii.sqlite - ensure hawaii.sqlite is already in place (in the same folder level as this file), or a new, blank file will be created
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"        
        f"/api/v1.0/<start>/<end>"        
        )       

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    date_format = "%Y-%m-%d"
    nonleap_year = 365
    query_date = dt.datetime.strptime(last_date, date_format) - dt.timedelta(days=nonleap_year)
    date_and_prcp = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date > query_date).\
                    order_by(Measurement.date).all()
    date_prcp_dict = dict(date_and_prcp)
    f"JSON list of dates and temperatures:<br/>"    
    return jsonify(date_prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(Station.name).all()
    f"JSON list of stations from the dataset:<br/>"
    session.close()
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    return "a JSON list of temperature observations"

@app.route("/api/v1.0/<start>")
def start(start):
    return "calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date"

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    return "calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive"

if __name__ == "__main__":
    app.run(debug=True)

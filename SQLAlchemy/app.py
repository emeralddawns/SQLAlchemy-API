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

# Returns the jsonified precipitation data for the last year in the database
# Returns json with the date as the key and the value as the precipitation
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
    f"JSON list of dates and precipitation (in):<br/>"
    session.close()
    return jsonify(date_prcp_dict)

# Returns jsonified data of all of the stations in the database
@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(Station.name).all()
    f"JSON list of stations from the dataset:<br/>"

    session.close()
    return jsonify(station_names)

# Returns jsonified data for the most active station for the last year of data
@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    date_format = "%Y-%m-%d"
    nonleap_year = 365
    query_date = dt.datetime.strptime(last_date, date_format) - dt.timedelta(days=nonleap_year)
    station_activity = session.query(Measurement.station, func.count(Measurement.station).label("Total"))\
                            .group_by(Measurement.station)\
                            .order_by(desc("Total")).all()
    active_station = max(station_activity, key=lambda x:x[1])    
    date_and_tobs = session.query(Measurement.date, Measurement.tobs)\
                    .filter(Measurement.date > query_date)\
                    .filter(Measurement.station == active_station[0]).all()
    date_tobs_dict = dict(date_and_tobs)
    f"JSON list of temperature observations from the most active station"

    session.close()
    return jsonify(date_tobs_dict)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    station_activity = session.query(Measurement.station, func.count(Measurement.station).label("Total"))\
                            .group_by(Measurement.station)\
                            .order_by(desc("Total")).all()
    active_station = max(station_activity, key=lambda x:x[1])

    TMIN = session.query(func.min(Measurement.tobs))\
                            .filter(Measurement.station == active_station[0])\
                            .filter(Measurement.date >= start_date).scalar()

    TAVG = session.query(func.max(Measurement.tobs))\
                            .filter(Measurement.station == active_station[0])\
                            .filter(Measurement.date >= start_date).scalar()

    TMAX = session.query(func.avg(Measurement.tobs))\
                            .filter(Measurement.station == active_station[0])\
                            .filter(Measurement.date >= start_date).scalar()

    print(f"calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date")
    return jsonify(lowest_temp), jsonify(highest_temp)









@app.route("/api/v1.0/<start>/<end>")
def startend(start_date, end_date):
    return "calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive"

if __name__ == "__main__":
    app.run(debug=True)

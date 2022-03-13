import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime
import time

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

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

# Create/binds our session (link) from Python to the DB
session = Session(engine)


app = Flask(__name__)

# CAN I MAKE THESE CLICKABLE LINKS?
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

    session.close()
    return jsonify(date_prcp_dict)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(Station.station, Station.name).all()
    all_stations = []
    for station, name in station_names:
            station_dict = {}
            station_dict["station"] = station
            station_dict["name"] = name

            all_stations.append(station_dict)
    session.close()
    return jsonify(all_stations)

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
    date_and_tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs)\
                    .filter(Measurement.date >= query_date)\
                    .filter(Measurement.station == active_station[0]).all()

    station_and_tobs = []
    for line in date_and_tobs :
            date_tobs_dict = {}
            date_tobs_dict["station"] = line[0]
            date_tobs_dict["date"] = line[1]
            date_tobs_dict["tobs"] = line[2]

            station_and_tobs.append(date_tobs_dict)
    session.close()
    return jsonify(station_and_tobs)

# Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
@app.route("/api/v1.0/<start_date>")
def start(start_date):
    temperatures = session.query(Measurement.date, func.avg(Measurement.tobs),func.min(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start_date)\
                            .group_by(Measurement.date).all()

    active_station = {}
    for line in temperatures:
        active_station[line[0]] = {"TMIN": line[2], "TAVG": round(line[1],1), "TMAX": line[3]}


    session.close()
    return jsonify(active_station)

# # Returns the min, max, and average temperatures calculated from the given start date to the given end date
@app.route("/api/v1.0/<start_date>/<end_date>")
def startend(start_date, end_date):

    temperatures = session.query(Measurement.date, func.avg(Measurement.tobs),func.min(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start_date)\
                            .filter(Measurement.date <= end_date)\
                            .group_by(Measurement.date).all()

    active_station = {}
    for line in temperatures:
        active_station[line[0]] = {"TMIN": line[2], "TAVG": round(line[1],1), "TMAX": line[3]}

    session.close()
    return jsonify(active_station)


if __name__ == "__main__":
    app.run(debug=True)

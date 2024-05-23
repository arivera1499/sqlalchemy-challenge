# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
station = base.classes.station

measurement = base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#variables to be used later in def's
recent_d = dt.date(2017, 8, 23)
year_before = dt.date(recent_d.year-1, recent_d.month, recent_d.day)

#landing page for api 
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate"
    )

#route for the precipitation link. code taken from ipynb file with list comprehension at the end to conver results to a dict.
@app.route("/api/v1.0/precipitation")
def precipitation():
   query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_before).all()
   precipitation = {date: prcp for date, prcp in query}#take from chat gpt
   return jsonify(precipitation)

#route for the list of stations link
@app.route("/api/v1.0/stations")
def stations():
    q2 = session.query(station.station).all()
    stations = list(np.ravel(q2))
    return jsonify(stations=stations)

#route for the temps of busiest station 
@app.route("/api/v1.0/tobs")
def temp_monthly():
    q3 = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= year_before).all()
    temps = list(np.ravel(q3))
    return jsonify(temps=temps)

#route for start date
@app.route("/api/v1.0/<start>")
def startnoend(start):
    q3 = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    temps2 = list(np.ravel(q3))
    return jsonify(temps2)

#route for start and end date
@app.route("/api/v1.0/<start>/<end>")
def startandend(start, end):
    q4 = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    temps3 = list(np.ravel(q4))
    return jsonify(temps3)

if __name__ == '__main__':
    app.run(debug=True)
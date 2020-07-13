#
# Set Up the Flask Weather App
#
# import dependencies 
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set Up the Database
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# create a session link from Python to our databas
session = Session(engine)

# Setup Flask 
app = Flask(__name__)
# Section 9.4.3 and Section 9.5.2 Create a Route
@app.route('/')
# def hello_world():
#    return 'Hello world'
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# 9.5.3 Percipitation Routes
# In order to run the app, first open Anaconda powershell prompt 
# then type $env:FLASK_APP="app.py"
# then type flask run
# Open a webpage and type http://127.0.0.1:5000/api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
       filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# 9.5.4 Stattions Route
# In order to run the app, first open Anaconda powershell prompt 
# then type $env:FLASK_APP="app.py"
# then type flask run
# Open a webpage and type http://127.0.0.1:5000/api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# 9.5.5 Monthly Temperature Route
# In order to run the app, first open Anaconda powershell prompt 
# then type $env:FLASK_APP="app.py"
# then type flask run
# Open a webpage and type http://127.0.0.1:5000/api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# 9.5.6 Statistics Route
# In order to run the app, first open Anaconda powershell prompt 
# then type $env:FLASK_APP="app.py"
# then type flask run
# Open a webpage and type http://127.0.0.1:5000//api/v1.0/temp/start/end 
# Open a webpage and type http://127.0.0.1:5000//api/v1.0/temp/2017-06-01/2017-06-30

@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end: 
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
           filter(Measurement.date >= start).\
               filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
 
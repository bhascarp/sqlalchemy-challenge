# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
app = Flask(__name__)
#################################################

#################################################
# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start-end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return 12 months of precipitation data"""
    # Query all passengers
    # results = session.query(Passenger.name).all()
    precipitation = []
    for date, prcp in df:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = precipitation
        precipitation.append(precipitation_dict)

    session.close()

    # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Stations"""
    # Query all passengers
    results = session.query(station.name).all()

    session.close()

    return jsonify(all_passengers)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Temperatures for last year"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').\
    filter(Measurement.station=='USC00519281').all()

    session.close()

    return jsonify(tobs)


@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Temperatures from a given start date"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').all()
    

    session.close()

    return jsonify(start)


@app.route("/api/v1.0/startend")
def startend():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Temparatues for a given time range"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').all()

    session.close()

    return jsonify(startend)


if __name__ == '__main__':
    app.run(debug=True)


#################################################

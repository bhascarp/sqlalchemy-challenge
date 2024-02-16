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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
# Base.prepare(autoload_with=engine)
Base.prepare(engine,reflect=True)
# Save references to each table
print(Base.classes.keys())
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
        "<div style='text-align: left; color: green; font-family: areal, sans-serif;'>"
        "<h1>Welcome to the API</h1>"
        "<p>Available Routes for Climate App"
        
        "<div style='display: flex; flex-direction: column; align-items: left;'>"
        f"<br/>1. <a href='/api/v1.0/precipitation'>/api/v1/0/precipitation</a><br/>"
        f"<br/>2. <a href='/api/v1.0/stations'>/api/v1/0/stations</a><br/>"
        f"<br/>For tobs, the data is listed for USC00519281<br/>"
        f"<br/>3. <a href='/api/v1.0/tobs'>/api/v1/0/tobs</a><br/>"
        f"<br/> For below, the date format example: 2016-08-23 <br/>"
        f"<br/> Here is sample url to try: http://127.0.0.1:8000/api/v1.0/2016-08-01"
        f"<br/>4. <a href='/api/v1.0/&lt;start&gt'>/api/v1/0/&lt;start&gt</a><br/>"
        f"<br/> For below, the date format example: 2016-08-23/2017-08-23 <br/>"
        f"<br/> Here is sample url to try: http://127.0.0.1:8000/api/v1.0/2016-09-01/2016-09-30"
        f"<br/>5. <a href='/api/v1.0/&lt;start&gt;/&lt;end&gt'>/api/v1/0/&lt;start&gt;/&lt;end&gt</a><br/>"

        "</div>"
        "/div>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the precipitation values
    last12 = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').\
    order_by(Measurement.date).all()

    session.close()

    """Return 12 months of precipitation data"""
 
    precipitation = []
    for date, prcp in last12:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)
    


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Stations"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Temperatures for last year at the most active station"""

    # Query the temperatures of the most active station for the previous year data
    queryresult = session.query( Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281')\
     .filter(Measurement.date>='2016-08-23').all()
    
    session.close()

    tob_obs = []
    for date, tobs in queryresult:
         tobs_dict = {}
         tobs_dict["Date"] = date
         tobs_dict["Tobs"] = tobs
         tob_obs.append(tobs_dict)

    return jsonify(tob_obs)



@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Temperatures from a given start date"""
    # Query the temperatures
    start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    
    session.close()

    start_list = []

    for min, avg, max in start_temp:
        start_dict = {}
        start_dict['min'] = min
        start_dict['avg'] = avg
        start_dict['max'] = max
        start_list.append(start_dict)

    return jsonify(start_list)



@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return minimum temperatue, maximum temperature and average temperature for a given time range"""
    # Query the temperatures
    start_end_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start). filter(Measurement.date <= end).all()

    session.close()

    start_end_list = []

    for min, avg, max in start_end_temp:
        start_end_dict = {}
        start_end_dict['min'] = min
        start_end_dict['avg'] = avg
        start_end_dict['max'] = max
        start_end_list.append(start_end_dict)

    return jsonify(start_end_list)


if __name__ == '__main__':
    app.run(debug=True)

#################################################

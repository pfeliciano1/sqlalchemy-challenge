import numpy as np
import datetime as dt

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
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2017-08-23"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    # Using the query from part 1 (most recent 12 months of precipitation data)
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Query all precipitations
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(prcp_data))

    # Return JSON List of Precipitations
    return jsonify(all_prcp)

# Stations Route
@app.route("/api/v1.0/stations")
def stations():

    # Query all passengers
    stations_data = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for name, station in stations_data:
        stations_dict = {}
        stations_dict["name"] = name
        stations_dict["station"] = station
        all_stations.append(stations_dict)
    
    # Return JSON List of Stations
    return jsonify(all_stations)

# Tobs Route
@app.route("/api/v1.0/tobs")
def tobs():
        # Query for the dates and temperature observations of the most active station for the most recent 12 months of data.
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        all_tobs = list(np.ravel(tobs_data))

        # Return JSON List of temperature observations (tobs) for the Previous Year
        return jsonify(all_tobs)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        # Create a query that returns the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_day_list = list(start_day)
        # Return a JSONified dictionary of these minimum, maximum, and average temperatures.
        return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        # Create a query that returns the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(start_end_day)
        # Return a JSONified dictionary of these minimum, maximum, and average temperatures.
        return jsonify(start_end_day_list)


if __name__ == '__main__':
    app.run(debug=True)

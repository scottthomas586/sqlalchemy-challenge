# import dependancies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#flask setup
app = Flask(__name__)

#flask routes
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"Date range is 2016-08-23 to 2017-08-23<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
)

@app.route("/api/v1.0/precipitation")
def names():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
            filter(Measurement.date <= "2017-08-24").all()

    session.close()

#create JSON list
    prcp_list = [results]

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Measurement.station, Station.name).\
        group_by(Station.name).all()

    session.close()

#create JSON list of stations
    station_list = [results]

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
            filter(Measurement.date >= "2016-08-23").\
                filter(Measurement.date <= "2017-08-23").all()
    
    session.close()

#create JSON list of tobs
    tobs = [results]

    return jsonify(tobs)

@app.route("/api/v1.0/yyyy-mm-dd/<start_date>")
def daily_normals(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    session.close()

    daily_normals = [results]

    return jsonify(daily_normals)

@app.route("/api/v1.0/yyyy-mm-dd/<start_date>/<end_date>")
def date_range(start_date, end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    date_range = [results]

    return jsonify(date_range)

if __name__ == '__main__':
    app.run(debug=True)



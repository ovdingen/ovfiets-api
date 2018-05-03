import sys
import json
from flask import Flask
import sqlite3


configfile = 'conf/daemon.json'

config = json.load(open(configfile))

app = Flask(__name__)

def dict_from_row(row):
    return dict(zip(row.keys(), row))

@app.route("/v1/station/<station_code>")
def station(station_code):
    db = sqlite3.connect(config['db'])
    db.row_factory = sqlite3.Row
    c = db.cursor()

    availability = {}
    
    rows = c.execute("SELECT * FROM availability WHERE stationcode = ?", [station_code])
    status = "OK"
    for row in rows:
        row_dict = dict_from_row(row)
        row_dict['openinghours'] = json.loads(row_dict['openinghours'])
        locationcode = row_dict['locationcode']
        row_dict.pop('locationcode')
        availability[locationcode] = row_dict

    if len(availability) is 0:
        status = "NOTFOUND"
    
    return_dict = {"status": status, "availability": availability}
    db.close()
    return json.dumps(return_dict)

@app.route("/v1/afgiftepunt/<afg_code>")
def afgiftepunt(afg_code):
    db = sqlite3.connect(config['db'])
    db.row_factory = sqlite3.Row
    c = db.cursor()

    availability = {}
    
    rows = c.execute("SELECT * FROM availability WHERE locationcode = ? LIMIT 1", [afg_code])
    status = "OK"
    for row in rows:
        row_dict = dict_from_row(row)
        row_dict['openinghours'] = json.loads(row_dict['openinghours'])
        locationcode = row_dict['locationcode']
        row_dict.pop('locationcode')
        availability[locationcode] = row_dict

    if len(availability) is 0:
        status = "NOTFOUND"
    
    return_dict = {"status": status, "availability": availability}
    db.close()
    return json.dumps(return_dict)

@app.route("/v1/total")
def total():
    db = sqlite3.connect(config['db'])
    db.row_factory = sqlite3.Row
    c = db.cursor()

    availability = {}
    
    rows = c.execute("SELECT * FROM availability")
    status = "OK"
    for row in rows:
        row_dict = dict_from_row(row)
        row_dict['openinghours'] = json.loads(row_dict['openinghours'])
        locationcode = row_dict['locationcode']
        row_dict.pop('locationcode')
        availability[locationcode] = row_dict

    if len(availability) is 0:
        status = "NOTFOUND"
    
    return_dict = {"status": status, "availability": availability}
    db.close()
    return json.dumps(return_dict)
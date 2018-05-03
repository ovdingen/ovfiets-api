import argparse
import zmq
import json
import zlib
import sqlite3

parser = argparse.ArgumentParser(description="Daemon for collecting OV-fiets availability")
parser.add_argument('config')

args = parser.parse_args()

config = json.load(open(args.config))

db_conn = sqlite3.connect(config['db'])

zmq_context = zmq.Context()
zmq_sock = zmq_context.socket(zmq.SUB)
zmq_sock.connect(config['addr'])
zmq_sock.setsockopt(zmq.SUBSCRIBE, '/OVfiets')

while True:
    c = db_conn.cursor()
    topic = zmq_sock.recv()

    message_gzip = zmq_sock.recv()
    message = json.loads(zlib.decompress(message_gzip, 16+zlib.MAX_WBITS))
    # Decompress gzip data, and convert resulting JSON to a dict

    if "stationCode" not in message:
        stationcode = ""
    else:
        stationcode = message["stationCode"].upper()

    if "openingHours" not in message:
        openinghours = []
    else:
        openinghours = message["openingHours"]

    if "description" not in message:
        description = ""
    else:
        description = message["description"]

    
    db_values = [message['extra']['locationCode'], stationcode, message["name"], message["extra"]["fetchTime"], message["extra"]["rentalBikes"], message["lat"], message["lng"], json.dumps(openinghours), description, message["open"]]
    c.execute("REPLACE INTO availability VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", db_values)
    db_conn.commit()

#!/usr/bin/env python3
import telnetlib
from datetime import datetime
import json
from pymongo import MongoClient
import os

# MongoDB Interface Configuration
_hostname=os.getenv('DB_HOST')
_port=os.getenv('DB_PORT')
_user=os.getenv('DB_USER')
_password=os.getenv('DB_PASS')
_dbname=os.getenv('DB_NAME')
print ("Connecting to DB: " + _hostname + " " + _port)

# Telnet Interface Configuration
HOST = os.getenv('SKIMMER_HOST')
PORT = os.getenv('SKIMMER_PORT')
user = os.getenv('SKIMMER_USER')
passw = os.getenv('SKIMMER_PASS')
timeout = 120 # seconds
print ("Connecting to telnet: " + HOST + " " + PORT)
tn = telnetlib.Telnet(HOST, port=PORT)


# Code
a = tn.read_until(b"Please enter your callsign:")
print (a)
tn.write(str.encode(user) + b"\n")
#if password: # TODO password protection
#    tn.read_until(b"Password: ")
#    tn.write(password.encode('ascii') + b"\n")

db = MongoClient('mongodb://'+_hostname+':'+str(_port)+'/', username=_user, password=_password)[_dbname]
collection = db['spots']


while 1 == 1:
    msg = tn.read_until(b"\n", timeout=timeout)

    # If a message has arrived, get timestamp
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    a = msg.decode("utf-8").split()
    print (msg)

    if (len(a) > 9): # If response contains a spot 
        tdate = str(dt).split()[0]
        ttime = str(dt).split()[1]
        b = {
            "frequency": a[3],
            "callsign": a[4],
            "snr": a[5],
            "wpm": a[7],
            "timestamp_skimmer" : a[-1],
            "timestamp_date": tdate,
            "timestamp_time": ttime,
            "timestamp": str(ts),
        }

        json_object = json.dumps(b, indent = 4) 
        print(json_object)

        collection.insert_one(b)

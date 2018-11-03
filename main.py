#!/usr/bin/python
#setting default directory
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from flask import Flask,request
import json
import atexit
from robot import handler

app = Flask(__name__)
handler.setup()

@app.route('/handler', methods=['POST'])
def handle():
    direction = request.get_json(force=True)
    print "direction:"+ str(direction)
    robot_status = handler.handle_wheels(direction)
    return json.dumps(robot_status)

@app.route('/status')
def status():
    sensors = handler.read_sensors()
    return json.dumps(sensors)

def app_shutdown():
    handler.terminate()	

atexit.register(app_shutdown)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)



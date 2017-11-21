#!/usr/bin/env python
""" server component to read and serve
sr1168c hex code from unit to json-web """

import os
import serial
from flask import Flask
from flask import jsonify
from pprint import pprint

bind_port = int(os.environ['BIND_PORT'])

def c_to_f(celcius):
    """Convert Celcius string to Fahrenheit"""
    fahrenheit = (celcius * 9 / 5) + 32
    return fahrenheit

app = Flask(__name__)  # pylint: disable=invalid-name

@app.route('/')
def index():
    """ index page function """
    serial_device = os.environ['SERIAL_DEVICE']
    if serial_device == '/dev/test':
        output = {'value': 'TEST OK'}
    else:
        ser = serial.Serial(serial_device, 4800)
        ser.write("\x01\x03\x00\x00\x00\x10\x14\x00")
        raw = ser.read(37)
        data = raw[3:37]
        output = {
            'temperature': {
                't0': c_to_f(ord(data[0]) - 10),
                't1': c_to_f(ord(data[1]) - 10),
                't2': c_to_f(ord(data[2])),
                't3': c_to_f(ord(data[3]))
             },
            'time': {
                'pump': (256 * ord(data[10]) + ord(data[11]))
            },
            'power': {
                 'e_kw': (256 * ord(data[12]) + ord(data[13])),
                 'e_accum_kw': (256 * ord(data[12]) + ord(data[15])),
                 'e_accum_mw': (256 * ord(data[12]) + ord(data[17]))
            },
            'state': {
                 'pump': int(ord(data[29]) & 0x01)
            }
        }
        pprint(output)
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=bind_port)

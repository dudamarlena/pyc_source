# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: robotreviewer/robot.py
# Compiled at: 2016-02-06 21:08:51
"""
RobotReviewer server

Simple Flask server, which takes in the full text of a clinical
trial in JSON format, e.g.:

{"text": "Streptomycin Treatment of Pulmonary Tuberculosis: A Medical Research Council Investigation..."}

and outputs Risk of Bias annotations in JSON format.

The JSON query should be sent as a POST query to:
`SERVER-NAME/annotate`
which by deafult would be localhost at:
`http://localhost:5000/annotate`

"""
import os, logging
from flask import Flask, json
from flask import redirect, url_for, jsonify
from flask import request
from biasrobot import BiasRobot

def str2bool(v):
    return v.lower() in ('yes', 'true', 't', '1')


DEBUG_MODE = str2bool(os.environ.get('DEBUG', 'false'))
LOG_LEVEL = logging.DEBUG if DEBUG_MODE else logging.INFO
logging.basicConfig(level=LOG_LEVEL, format='[%(levelname)s] %(name)s %(asctime)s: %(message)s')
log = logging.getLogger(__name__)
app = Flask(__name__, static_url_path='')
app.debug = DEBUG_MODE
log.info('Welcome to RobotReviewer :)')
log.info('loading models')
BOT = BiasRobot()
log.info('done loading models')

@app.route('/')
def main():
    return redirect(url_for('static', filename='index.html'))


@app.route('/annotate', methods=['POST'])
def annotate():
    json_data = request.json
    annotations = BOT.annotate(json_data['text'])
    return json.dumps(annotations)


def run():
    app.run()
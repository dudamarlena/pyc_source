# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thrift4DL/server/http/api.py
# Compiled at: 2020-01-17 02:20:48
# Size of source mod 2**32: 755 bytes
from flask import Flask
from flask import render_template, request
import json, traceback
from thrift4DL.client import VisionClient
APP_NAME = 'RESTful-Thrift4DL'

def create_app(host, port):
    app = Flask(APP_NAME)

    @app.route('/v1/predict/', methods=['POST'])
    def predict():
        pred_result = {'error_code':-1,  'error_message':'Failed',  'content':''}
        try:
            client = VisionClient(host=host, port=port)
            pred_result = client.predict(request.data.decode('utf-8'))
        except:
            print(traceback.format_exc())

        return json.dumps(pred_result)

    return app
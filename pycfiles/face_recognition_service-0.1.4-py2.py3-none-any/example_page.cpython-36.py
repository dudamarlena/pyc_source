# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kedpter/KHome/WorkStation/Proj/FaceRecognitionPenaltySystem/face_recognition_service/face_recognition_service/resources/example_page.py
# Compiled at: 2019-12-24 21:49:43
# Size of source mod 2**32: 336 bytes
from flask_restful import Resource, reqparse
import werkzeug, tempfile
from flask import render_template, make_response

class ExamplePage(Resource):

    def __init__(self):
        pass

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)
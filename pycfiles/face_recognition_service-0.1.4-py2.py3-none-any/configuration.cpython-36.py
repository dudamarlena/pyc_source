# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kedpter/KHome/WorkStation/Proj/FaceRecognitionPenaltySystem/face_recognition_service/face_recognition_service/resources/configuration.py
# Compiled at: 2019-11-24 20:56:01
# Size of source mod 2**32: 458 bytes
from flask_restful import Resource, reqparse, inputs
from face_recognition_service.face_engine import FaceEngine

class Configuration(Resource):

    def put(self):
        parse = reqparse.RequestParser()
        parse.add_argument('enable_cnn', type=(inputs.boolean), required=True, location='args')
        args = parse.parse_args()
        engine = FaceEngine()
        engine.enable_cnn = args['enable_cnn']
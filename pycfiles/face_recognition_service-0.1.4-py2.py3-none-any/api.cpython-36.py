# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kedpter/KHome/WorkStation/Proj/FaceRecognitionPenaltySystem/face_recognition_service/face_recognition_service/api.py
# Compiled at: 2020-01-17 03:40:28
# Size of source mod 2**32: 1303 bytes
"""
This module functions as an adapter. It will direct user request to specific api controller
"""
from flask import Flask
from flask_restful import Resource, Api
import os
from .resources.encodings import FaceEncodingList, FaceEncoding
from face_recognition_service.resources.conversion import Conversion
from face_recognition_service.resources.comparison import CompareDistances
from face_recognition_service.resources.configuration import Configuration
from face_recognition_service.resources.example_page import ExamplePage
app = Flask(__name__, static_folder='static')
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
app.config['convert_faces_dir'] = '{}/static/convert_faces'.format(BASE_DIR)
api = Api(app)
__version__ = 'v1'
api_version = '/{0}/{1}'.format('api', __version__)
face_module = '{0}/{1}'.format(api_version, 'face')
api.add_resource(FaceEncodingList, '{0}/encodings'.format(face_module))
api.add_resource(FaceEncoding, '{0}/encodings/<encoding_id>'.format(face_module))
api.add_resource(Conversion, '{0}/conversions/encoding'.format(face_module))
api.add_resource(CompareDistances, '{0}/comparison/distances'.format(face_module))
api.add_resource(Configuration, '{0}/configuration'.format(face_module))
api.add_resource(ExamplePage, '/')
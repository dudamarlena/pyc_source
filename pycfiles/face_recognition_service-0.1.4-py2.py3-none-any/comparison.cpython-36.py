# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kedpter/KHome/WorkStation/Proj/FaceRecognitionPenaltySystem/face_recognition_service/face_recognition_service/resources/comparison.py
# Compiled at: 2020-01-17 03:01:21
# Size of source mod 2**32: 1162 bytes
from flask_restful import Resource, reqparse
import werkzeug, tempfile, numpy as np
from flask import jsonify
import os
from face_recognition_service.face_engine import FaceEngine

class CompareDistances(Resource):

    def post(self):
        """
        compare distances between an unknown face and known faces
        """
        parse = reqparse.RequestParser()
        parse.add_argument('tolerance',
          type=float, required=True, location='form')
        parse.add_argument('unknown_dat',
          required=True, type=(werkzeug.datastructures.FileStorage), location='files')
        args = parse.parse_args()
        engine = FaceEngine()
        with tempfile.NamedTemporaryFile(delete=False) as (tmp):
            tmp.write(args['unknown_dat'].read())
            tmp.flush()
            tmp.seek(0)
            unknown_encoding = np.load((tmp.name), allow_pickle=True)
            distances_json = engine.face_distance(unknown_encoding)
            filtered = {str(k):v for k, v in distances_json.items() if v <= args['tolerance']}
            tmp.close()
            os.unlink(tmp.name)
            return jsonify(filtered)
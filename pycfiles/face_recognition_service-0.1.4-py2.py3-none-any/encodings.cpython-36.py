# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kedpter/KHome/WorkStation/Proj/FaceRecognitionPenaltySystem/face_recognition_service/face_recognition_service/resources/encodings.py
# Compiled at: 2020-01-17 03:02:21
# Size of source mod 2**32: 1705 bytes
from flask_restful import Resource, reqparse
from flask import json, Response
import werkzeug, tempfile
from face_recognition_service.face_engine import FaceEngine
from face_recognition_service.models.face import DbException
import numpy as np, os

class FaceEncodingList(Resource):

    def delete(self):
        """
        delete all encodings
        """
        engine = FaceEngine()
        engine.delete_all_encodings()

    def post(self):
        """
        add an encoding
        """
        parse = reqparse.RequestParser()
        parse.add_argument('id', type=int, required=True, location='form')
        parse.add_argument('encoding_file',
          required=True, type=(werkzeug.datastructures.FileStorage), location='files')
        args = parse.parse_args()
        engine = FaceEngine()
        with tempfile.NamedTemporaryFile(delete=False) as (tmp):
            tmp.write(args['encoding_file'].read())
            tmp.flush()
            tmp.seek(0)
            face_encoding = np.load((tmp.name), allow_pickle=True)
            tmp.close()
            os.unlink(tmp.name)
            try:
                engine.add_face(args['id'], face_encoding)
            except DbException as e:
                msg = {'message': str(e)}
                return Response(response=(json.dumps(msg)),
                  status=500,
                  mimetype='application/json')


class FaceEncoding(Resource):

    def delete(self, encoding_id):
        """
        delete encoding by id
        """
        engine = FaceEngine()
        engine.delete_by_id(encoding_id)
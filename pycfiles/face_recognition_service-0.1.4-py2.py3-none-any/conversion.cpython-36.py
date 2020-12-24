# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kedpter/KHome/WorkStation/Proj/FaceRecognitionPenaltySystem/face_recognition_service/face_recognition_service/resources/conversion.py
# Compiled at: 2020-01-17 03:03:32
# Size of source mod 2**32: 1863 bytes
from flask_restful import Resource, reqparse
import werkzeug, tempfile, numpy as np, uuid
from face_recognition_service.face_engine import FaceEngine
from flask import send_file, current_app as app
import os

class Conversion(Resource):

    def post(self):
        """
        post an image file
        return a file of numpy face encoding array
        """
        parse = reqparse.RequestParser()
        parse.add_argument('face_image', required=True, type=(werkzeug.datastructures.FileStorage),
          location='files')
        args = parse.parse_args()
        engine = FaceEngine()
        with tempfile.NamedTemporaryFile(delete=False) as (tmp):
            file = args['face_image']
            tmp.write(file.read())
            tmp.flush()
            image = engine.load_image_file(tmp.name)
            tmp.close()
            os.unlink(tmp.name)
            encodings = engine.face_encodings(image)
            if len(encodings) == 0:
                return {'success':'false',  'reason':'no face in image'}
            else:
                encoding = encodings[0]
                np_file = '{0}/{1}.npy'.format(app.config['convert_faces_dir'], uuid.uuid1())
                np.save(np_file, encoding)
                file_handle = open(np_file, 'rb')

                def stream_and_remove_file():
                    yield from file_handle
                    file_handle.close()
                    os.remove(np_file)
                    if False:
                        yield None

                return app.response_class((stream_and_remove_file()),
                  mimetype='octet-stream',
                  headers={'Content-Disposition':'attachment', 
                 'filename':'face.dat'})
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kedpter/KHome/WorkStation/Proj/FaceRecognitionPenaltySystem/face_recognition_service/face_recognition_service/cli.py
# Compiled at: 2019-12-01 22:11:07
# Size of source mod 2**32: 391 bytes
from face_recognition_service.api import app
from face_recognition_service.face_engine import FaceEngine
import os

def main():
    app.debug = True
    FaceEngine().debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
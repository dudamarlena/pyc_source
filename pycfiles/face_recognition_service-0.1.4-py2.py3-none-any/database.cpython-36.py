# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kedpter/KHome/WorkStation/Proj/FaceRecognitionPenaltySystem/face_recognition_service/face_recognition_service/models/database.py
# Compiled at: 2019-11-24 20:56:01
# Size of source mod 2**32: 381 bytes
from face_recognition_service.models.face import FaceDao
from face_recognition_service.util.singleton import Singleton

class MemDatabase(metaclass=Singleton):

    def __init__(self):
        self.face_dao = FaceDao()

    def __str__(self):
        return '\n'.join([str(u) for u in self.face_dao.findall()])
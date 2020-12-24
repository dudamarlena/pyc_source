# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kedpter/KHome/WorkStation/Proj/FaceRecognitionPenaltySystem/face_recognition_service/face_recognition_service/face_engine.py
# Compiled at: 2019-12-01 22:11:48
# Size of source mod 2**32: 2753 bytes
from __future__ import print_function
import sys, face_recognition
from face_recognition_service.models.database import MemDatabase
from face_recognition_service.models.face import Face

class FaceEngine:
    _FaceEngine__shared_state = {}

    def __init__(self):
        self.__dict__ = self._FaceEngine__shared_state
        self.load_image_file_mode = 'RGB'
        self.tolerance = 0.6
        self.enable_cnn = False
        self._FaceEngine__db = MemDatabase()
        self.debug = True

    @property
    def faces(self):
        return self._FaceEngine__db.face_dao.find_all()

    def load_image_file(self, file):
        return face_recognition.load_image_file(file, self.load_image_file_mode)

    def face_encodings(self, face_image, known_face_locations=None, num_jitters=1):
        """
        :return: A list of 128-dimensional face encodings (one for each face in the image)
        """
        if self.enable_cnn:
            if known_face_locations is None:
                known_face_locations = face_recognition.face_locations(face_image, model='cnn')
        return face_recognition.face_encodings(face_image, known_face_locations, num_jitters)

    def face_distance(self, face_to_compare):
        """
        Given a list of face encodings from database, compare them to a known face encoding and get a euclidean distance
        for each comparison face. The distance tells you how similar the faces are.

        :param face_to_compare: A face encoding to compare against
        :return: a json array with id and distance
        """
        face_encodings = [x.encoding for x in self.faces]
        distances = face_recognition.face_distance(face_encodings, face_to_compare)
        result = {}
        for x in zip(self.faces, distances):
            result[x[0].id] = x[1]

        return result

    def compare_faces(self, face_distances):
        if self.debug:
            print('compare face', file=(sys.stdout))
        return list(face_distances <= self.tolerance)

    def delete_all_encodings(self):
        self._FaceEngine__db.face_dao.delete_all()
        if self.debug:
            print('delete all faces', file=(sys.stdout))

    def delete_by_id(self, id):
        self.debug
        self._FaceEngine__db.face_dao.delete_by_id(id)
        if self.debug:
            print(('delete face: {}'.format(id)), file=(sys.stdout))

    def add_face(self, id, encoding):
        f = Face(id, encoding)
        self._FaceEngine__db.face_dao.append(f)
        if self.debug:
            print(('add face: {}'.format(id)), file=(sys.stdout))
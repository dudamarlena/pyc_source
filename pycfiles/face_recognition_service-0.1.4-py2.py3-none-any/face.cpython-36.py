# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kedpter/KHome/WorkStation/Proj/FaceRecognitionPenaltySystem/face_recognition_service/face_recognition_service/models/face.py
# Compiled at: 2019-12-26 22:06:22
# Size of source mod 2**32: 995 bytes


class DbException(Exception):
    pass


class Face:

    def __init__(self, id, encoding):
        self.id = id
        self.encoding = encoding

    def __str__(self):
        return '[id]: {0}\n[encoding]: {1}'.format(self.id, self.encoding)


class FaceDao:

    def __init__(self):
        self._FaceDao__faces = []

    def __validate(self, obj):
        if not isinstance(obj, Face):
            raise DbException('Not a Face object')
        if any(x.id == obj.id for x in self._FaceDao__faces):
            raise DbException('id ({}) already exists'.format(obj.id))

    def append(self, obj):
        self._FaceDao__validate(obj)
        self._FaceDao__faces.append(obj)

    def extend(self, obj_list):
        for obj in obj_list:
            self._FaceDao__validate(obj)

        self._FaceDao__faces.extend(obj_list)

    def delete_by_id(self, id):
        self._FaceDao__faces = [f for f in self._FaceDao__faces if f.id != id]

    def delete_all(self):
        self._FaceDao__faces = []

    def find_all(self):
        return self._FaceDao__faces
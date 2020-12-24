# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/informer/utils.py
# Compiled at: 2020-05-08 00:01:07
# Size of source mod 2**32: 856 bytes
import json
from .config import PORT_DICT
if 'vision' in PORT_DICT.keys():
    import cv2

    def encode_img(img, isGrey=False):
        if isGrey:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=(cv2.INTER_AREA))
        ret, jpeg = cv2.imencode('.jpg', img)
        data = jpeg.tobytes()
        return data


def encode_sensor(v, w, c):
    data = {'v':v,  'w':w,  'c':c}
    data = json.dumps(data).encode()
    return data


def encode_message(data, robot_id, mtype='normal', pri=5):
    data = {'Mtype':mtype, 
     'Pri':pri,  'Id':robot_id,  'Data':data}
    data = json.dumps(data).encode()
    return data


def to_json(**kwargs):
    return json.dumps(kwargs)


def encode_debug_message(messages):
    data = json.dumps(messages).encode()
    return data
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/microsoft_demo.py
# Compiled at: 2018-08-21 05:25:16
import cognitive_face as CF, json, numpy as np, sys
from zprint import *

def init():
    KEY = '8f7fbf07deb944258ff459ef22b1fac2'
    CF.Key.set(KEY)
    BASE_URL = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0'
    CF.BaseUrl.set(BASE_URL)
    return CF


def detect(CF, img_url):
    try:
        result = CF.face.detect(img_url)
        return result
    except Exception as e:
        eprint('%s' % e)
        eprint('img_url:%s' % img_url)
        return []


def ms_face_detect(img_url):
    CF = init()
    result = detect(CF, img_url)
    cc = 0
    rects = []
    faceids = []
    for re in result:
        cc += 1
        rer = re['faceRectangle']
        rects.append(np.array((rer['left'], rer['top'], rer['width'], rer['height'])))
        faceids.append(re['faceId'])

    return rects


def ms_face_verify(CF, img_url1, img_url2):
    result1 = detect(CF, img_url1)
    result2 = detect(CF, img_url2)
    confidence_list = []
    for re1 in result1:
        for re2 in result2:
            vr = CF.face.verify(re1['faceId'], re2['faceId'])
            confidence = vr['confidence']
            confidence_list.append(confidence)

    return confidence_list


img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
img_url2 = '/data1/mingmingzhao/label/data_sets_teacher_1w/47017613_1510574400_out-video-jzc70f41fa6f7145b4b66738f81f082b65_f_1510574403268_t_1510575931221.flv_0001.jpg'
CF = init()
cl = ms_face_verify(CF, img_url, img_url2)
print cl
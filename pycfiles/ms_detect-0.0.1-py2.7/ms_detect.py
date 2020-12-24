# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ms_detect.py
# Compiled at: 2018-08-03 01:28:16
import cognitive_face as CF, json, numpy as np

def ms_face_detect(img_url):
    KEY = '6a78402ab44140aba9e2014e0c7263ea'
    CF.Key.set(KEY)
    BASE_URL = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0'
    CF.BaseUrl.set(BASE_URL)
    try:
        result = CF.face.detect(img_url)
    except Exception as e:
        print e
        return ms_face_detect(img_url)

    cc = 0
    rects = []
    for re in result:
        cc += 1
        rer = re['faceRectangle']
        rects.append(np.array((rer['left'], rer['top'], rer['width'], rer['height'])))

    return rects


img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
img_url = '/data1/mingmingzhao/label/data_sets_teacher_1w/47017613_1510574400_out-video-jzc70f41fa6f7145b4b66738f81f082b65_f_1510574403268_t_1510575931221.flv_0001.jpg'
print ms_face_detect(img_url)
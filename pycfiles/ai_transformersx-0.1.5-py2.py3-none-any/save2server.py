# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/save2server.py
# Compiled at: 2018-08-04 12:36:17
import cv2

def save2server(imgname, img):
    ret = cv2.imwrite('/data1/mingmingzhao/data_sets/test/race_recog/' + imgname, img)
    ret = cv2.imwrite(imgname, img)
    print ('local url is /data1/mingmingzhao/data_sets/test/race_recog/{}').format(imgname)
    print ('remote url is http://192.168.7.37:8393/static/race_recog/{}').format(imgname)
    print ("<img src='http://192.168.7.37:8393/static/race_recog/{}' title={} />").format(imgname, imgname)
    print ('or u can view the image at :http://192.168.7.37:8393/show/?start_num=1&length=200&dirname=/{}').format(imgname.split('/')[:-1])
    return ret
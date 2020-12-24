# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
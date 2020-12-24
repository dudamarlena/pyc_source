# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\flv2img\flv2img.py
# Compiled at: 2018-08-13 07:42:17
import cv2, os

def flv2img(flv='ceshivedio.flv', count=5, star=1, end=100):
    list_all = []
    vc = cv2.VideoCapture(flv)
    c = 1
    if vc.isOpened():
        rval = True
    else:
        rval = False
    while rval:
        rval, frame = vc.read()
        if c % count == 0:
            if c / count >= star and c / count <= end:
                list_all.append(frame)
        c += 1

    print list_all
    print 'there are %d pictures' % len(list_all)
    return list_all
    vc.release()


if __name__ == '__main__':
    flv2img()
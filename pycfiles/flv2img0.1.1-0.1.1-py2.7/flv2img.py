# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\flv2img\flv2img.py
# Compiled at: 2018-08-13 08:37:35
import cv2, os

def flv2img(flv='ceshivedio.flv', count=2, star=1, end=100):
    list_all = []
    vc = cv2.VideoCapture(flv)
    c = 1
    fps = dps(flv)
    fps = int(fps / count)
    if vc.isOpened():
        rval = True
    else:
        rval = False
    j = 0
    while rval:
        rval, frame = vc.read()
        if c % fps == 0:
            if c / fps >= star and c / fps <= end:
                j += 1
                list_all.append(frame)
        c += 1
        if j > end:
            break

    if j < end - star + 1:
        print 'Sorry,pictures are not enough'
    print 'there are %d pictures' % len(list_all)
    return list_all
    vc.release()


def dps(vedio):
    video = cv2.VideoCapture(vedio)
    major_ver, minor_ver, subminor_ver = cv2.__version__.split('.')
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    return fps


if __name__ == '__main__':
    flv2img()
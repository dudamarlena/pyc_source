# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\flv2img\flv2img.py
# Compiled at: 2018-08-14 05:43:48
import cv2, os
from vcvf import face_detector as fd
import math

def faceimg(flv='ceshivedio.flv', rate=0.3, star=1, end=100):
    face = flv2img(flv, rate, star, end)
    fd1 = fd.face_detector(2)
    face_list = []
    for i in range(len(face)):
        img = face[i]
        try:
            num, list1, time = fd1.detect_face(img)
        except Exception as e:
            print e
            num = 0

        if num >= 1:
            face_list.append(img)

    print 'there are %d face pictures' % len(face_list)
    return face_list


def flv2img(flv='ceshivedio.flv', rate=0.3, star=1, end=100):
    list_all = []
    vc = cv2.VideoCapture(flv)
    c = 1
    fps = dps(flv)
    fps = fps / rate
    if vc.isOpened():
        rval = True
    else:
        rval = False
    j = 1
    count = 0.0
    while rval:
        count = fps * (j - 1)
        rval, frame = vc.read()
        if c - 1 == int(count):
            j += 1
            if math.floor(c / fps) >= star and math.floor(c / fps) <= end:
                if frame is not None:
                    list_all.append(frame)
        c += 1
        if len(list_all) > end:
            break

    if len(list_all) < end - star + 1:
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
    faceimg()
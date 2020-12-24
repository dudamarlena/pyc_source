# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/video2img.py
# Compiled at: 2018-11-06 06:39:45
import cv2, os
from vcvf import face_detector as fd
import math, threading, time
from zprint import *
import numpy as np, pdb

def faceimg(flv='ceshivedio.flv', rate=0.3, star=1, end=100):
    start_time = time.time()
    fd1 = fd.face_detector()
    face = flv2img(flv, rate, star, end)
    face_list = []
    for i in range(len(face)):
        img = face[i]
        try:
            num, list1, timecost = fd1.detect_face(img)
        except Exception as e:
            zprint(e)
            num = 0

        if num >= 1:
            face_list.append(img)

    elapse_time = time.time() - start_time
    zprint('faceimg use time:%f,face_number:%d/%d' % (elapse_time, len(face_list), len(face)))
    return (
     face_list, elapse_time)


def fiter_face(imglist, fdd):
    t1 = time.time()
    list(map(lambda x: fdd.detect_face(x), imglist))
    t2 = time.time()
    print t2 - t1


def fiter_face1(face, fdd):
    start_time = time.time()
    face_list = []
    for i in range(len(face)):
        img = face[i]
        try:
            num, list1, timecost = fdd.detect_face(img)
        except Exception as e:
            zprint(e)
            num = 0

        if num >= 1:
            face_list.append(img)

    elapse_time = time.time() - start_time
    zprint('faceimg use time:%f,face_number:%d/%d' % (elapse_time, len(face_list), len(face)))


def flv2img(flv='ceshivedio.flv', rate=0.3, star=1, end=100):
    list_all = []
    vc = cv2.VideoCapture(flv)
    c = 1
    fps = dps(flv)
    if rate > fps:
        zprint('the fps is %s, set the rate=fps' % fps)
        rate = fps
    if vc.isOpened():
        rval = True
    else:
        rval = False
    j = 1.0
    count = 0.0
    while rval:
        count = fps / rate * (j - 1)
        rval, frame = vc.read()
        if c - 1 == int(count):
            j += 1
            if math.floor(c / fps) >= star and math.floor(c / fps) < end:
                if frame is not None:
                    list_all.append(frame)
        c += 1
        if math.floor(c / fps) >= end:
            break

    zprint("[ %d ] pictures from '%s' " % (len(list_all), flv))
    vc.release()
    return list_all


def flv2img_wget(flv='ceshivedio.flv', rate=0.3, star=1, end=100):
    zprint('start donwload: %s' % flv)
    os.system('wget %s -q -O tmp.v' % flv)
    zprint('complete donwload: %s' % flv)
    return flv2img('tmp.v', rate, star, end)


def video2img(flv, rate=0.3, star=1, end=100):
    vc = cv2.VideoCapture(flv)
    fps = dps(flv)
    rval = vc.isOpened()


def dps(vedio):
    video = cv2.VideoCapture(vedio)
    major_ver, minor_ver, subminor_ver = cv2.__version__.split('.')
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    return fps


if __name__ == '__main__':
    fd1 = fd.face_detector()
    videofile = '/data1/case_study65/flvs/video/student/20180502/97535447_1525257000_out-video-jz320d98a2e0e04390be9aa2c8e4c42e8a_f_1525258221981_t_1525258392191.flv'
    videofile = 'https://vps-ve.vipkid.com.cn/videoedit/prod/projects/fifthanniversary/6978981/fifth_anniversary_6978981_final_video.mp4'
    imglist = flv2img_wget(videofile, 0.01, 1.5, 120.3)
    fiter_face(imglist, fd1)
    fiter_face1(imglist, fd1)
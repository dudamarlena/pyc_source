# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vcvf_emotion/face_emotion.py
# Compiled at: 2018-08-01 13:23:07
from keras.models import Sequential
from keras.layers import Dense
from sklearn.cross_validation import train_test_split
import numpy
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
import numpy as np
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
import matplotlib.pyplot as plt, numpy, sys, os, dlib, glob
try:
    import cPickle as pickle
except ImportError:
    import pickle

import random, cv2, datetime as dt, time, shutil, numpy as np, cv2, os
from distutils.sysconfig import get_python_lib
import time as tm
from face_utils.facealigner import FaceAligner
import time

class face_emotion:

    def __init__(self):
        self.site_package = get_python_lib()
        protofilename = os.path.join(self.site_package, 'vcvf_emotion/models/happymodle.json')
        weightfilename = os.path.join(self.site_package, 'vcvf_emotion/models/weights.best.hdf5')
        self.model = self.loadmodel(protofilename, weightfilename)
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.predictor_path = 'landmarks_68.dat'
        url = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
        self.predictor_path = self.get_model(url, self.predictor_path)
        self.sp = dlib.shape_predictor(self.predictor_path)
        self.fa = FaceAligner(self.sp, desiredFaceWidth=48)
        self.fa35 = FaceAligner(self.sp, desiredFaceWidth=48, desiredLeftEye=(0.27,
                                                                              0.27))
        self.detector = dlib.get_frontal_face_detector()

    def get_model(self, url, predictor_path):
        if not os.path.exists(predictor_path):
            print os.path.exists('%s.bz2' % predictor_path)
            if not os.path.exists('%s.bz2' % predictor_path):
                os.system('wget -O %s.bz2 %s' % (predictor_path, url))
            os.system('bunzip2 %s.bz2' % predictor_path)
        return predictor_path

    def loadmodel(self, protofilename, weightfilename):
        yaml_file = open(protofilename, 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        loaded_model = model_from_json(loaded_model_yaml)
        loaded_model.load_weights(weightfilename)
        return loaded_model

    def rect_dlib2opencv(self, d):
        return [
         d.left(), d.top(), d.right(), d.bottom()]

    def rect_opencv2dlib(self, rect):
        return dlib.rectangle(rect[0], rect[1], rect[2], rect[3])

    def face_emotion_rect(self, image, rect):
        ts = time.time()
        happy_score = 0.5
        d = self.rect_opencv2dlib(rect)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faceAligned = self.fa.align(image, gray, d)
        feature = faceAligned.reshape(2304)
        X = feature.reshape((1, 48, 48, 1))
        score = self.model.predict(X)
        te = time.time()
        happy_score = score[0][0]
        return (happy_score, d, te - ts)

    def get_align_face(self, image):
        fal = []
        dets = self.detector(image, 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for k, d in enumerate(dets):
            faceAligned = self.fa35.align(image, gray, d)
            fal.append(faceAligned)

        return fal

    def face_emotion(self, image):
        ts = time.time()
        sl = []
        dl = []
        dets = self.detector(image, 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for k, d in enumerate(dets):
            rect_tmp = [
             d.left(), d.top(), d.right(), d.bottom()]
            score, tc, d = self.face_emotion_rect(image, rect_tmp)
            sl.append(score)
            dl.append(d)

        te = time.time()
        return (sl, dl, te - ts)

    def face_emotion_flat(self, image):
        ts = time.time()
        flag = str(False)
        d = None
        sl, dl, tc = self.face_emotion(image)
        for i in range(0, len(sl)):
            if sl[i] > 0.5:
                flag = str(True)
                d = dl[i]
                break

        te = time.time()
        return (flag, d, te - ts)

    def test(self):
        fs = face_emotion()
        imf = os.path.join(self.site_package, 'vcvf_emotion/test.jpg')
        print imf
        image = cv2.imread(imf)
        print fs.face_emotion_rect(image, [91, 91, 180, 181])


def log2(message, of):
    print message
    of.write(message)


def draw_rect(img, savepath, left, top, right, bottom):
    cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 3)
    cv2.imwrite(savepath, img)
    return img


if __name__ == '__main__':
    dirname = '/data1/mingmingzhao/data_sets/hand_data/test_images/'
    dirname1 = '/data1/mingmingzhao/data_sets/face_emotion_data/neutral_images_all/origin_images_api_result/'
    fs = face_emotion()
    ci = 0
    ch = 0
    ts = 0
    for f in os.listdir(dirname):
        if f.endswith('.jpg'):
            imf = os.path.join(dirname, f)
            print imf
            image = cv2.imread(imf)
            rect = []
            print fs.face_emotion_flat(image)
            score, rect, tc = fs.face_emotion(image)
            if len(score):
                if score[0]:
                    print score
                    print os.path.join(dirname1, f)
                    print cv2.imwrite(os.path.join(dirname1, str(score[0]) + f), image)
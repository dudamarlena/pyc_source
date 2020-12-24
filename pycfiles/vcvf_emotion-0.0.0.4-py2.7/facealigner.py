# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vcvf_emotion/face_utils/facealigner.py
# Compiled at: 2018-08-01 08:04:54
from helpers import FACIAL_LANDMARKS_IDXS
from helpers import shape_to_np
import numpy as np, cv2

class FaceAligner:

    def __init__(self, predictor, desiredLeftEye=(0.15, 0.15), desiredFaceWidth=256, desiredFaceHeight=None):
        self.predictor = predictor
        self.desiredLeftEye = desiredLeftEye
        self.desiredFaceWidth = desiredFaceWidth
        self.desiredFaceHeight = desiredFaceHeight
        if self.desiredFaceHeight is None:
            self.desiredFaceHeight = self.desiredFaceWidth
        return

    def align(self, image, gray, rect):
        shape = self.predictor(gray, rect)
        shape = shape_to_np(shape)
        lStart, lEnd = FACIAL_LANDMARKS_IDXS['left_eye']
        rStart, rEnd = FACIAL_LANDMARKS_IDXS['right_eye']
        leftEyePts = shape[lStart:lEnd]
        rightEyePts = shape[rStart:rEnd]
        leftEyeCenter = leftEyePts.mean(axis=0).astype('int')
        rightEyeCenter = rightEyePts.mean(axis=0).astype('int')
        dY = rightEyeCenter[1] - leftEyeCenter[1]
        dX = rightEyeCenter[0] - leftEyeCenter[0]
        angle = np.degrees(np.arctan2(dY, dX)) - 180
        desiredRightEyeX = 1.0 - self.desiredLeftEye[0]
        dist = np.sqrt(dX ** 2 + dY ** 2)
        desiredDist = desiredRightEyeX - self.desiredLeftEye[0]
        desiredDist *= self.desiredFaceWidth
        scale = desiredDist / dist
        eyesCenter = (
         (leftEyeCenter[0] + rightEyeCenter[0]) // 2,
         (leftEyeCenter[1] + rightEyeCenter[1]) // 2)
        M = cv2.getRotationMatrix2D(eyesCenter, angle, scale)
        tX = self.desiredFaceWidth * 0.5
        tY = self.desiredFaceHeight * self.desiredLeftEye[1]
        M[(0, 2)] += tX - eyesCenter[0]
        M[(1, 2)] += tY - eyesCenter[1]
        w, h = self.desiredFaceWidth, self.desiredFaceHeight
        output = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC)
        outputgray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        return outputgray
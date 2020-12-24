# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xl_tensorflow\metrics\rafaelpadilla\BoundingBox.py
# Compiled at: 2020-04-06 00:22:57
# Size of source mod 2**32: 6983 bytes
from .utils import *

class BoundingBox:

    def __init__(self, imageName, classId, x, y, w, h, typeCoordinates=CoordinatesType.Absolute, imgSize=None, bbType=BBType.GroundTruth, classConfidence=None, format=BBFormat.XYWH):
        """Constructor.
        Args:
            imageName: String representing the image name.
            classId: String value representing class id.
            x: Float value representing the X upper-left coordinate of the bounding box.
            y: Float value representing the Y upper-left coordinate of the bounding box.
            w: Float value representing the width bounding box.
            h: Float value representing the height bounding box.
            typeCoordinates: (optional) Enum (Relative or Absolute) represents if the bounding box
            coordinates (x,y,w,h) are absolute or relative to size of the image. Default:'Absolute'.
            imgSize: (optional) 2D vector (width, height)=>(int, int) represents the size of the
            image of the bounding box. If typeCoordinates is 'Relative', imgSize is required.
            bbType: (optional) Enum (Groundtruth or Detection) identifies if the bounding box
            represents a ground truth or a detection. If it is a detection, the classConfidence has
            to be informed.
            classConfidence: (optional) Float value representing the confidence of the detected
            class. If detectionType is Detection, classConfidence needs to be informed.
            format: (optional) Enum (BBFormat.XYWH or BBFormat.XYX2Y2) indicating the format of the
            coordinates of the bounding boxes. BBFormat.XYWH: <left> <top> <width> <height>
            BBFormat.XYX2Y2: <left> <top> <right> <bottom>.
        """
        self._imageName = imageName
        self._typeCoordinates = typeCoordinates
        if typeCoordinates == CoordinatesType.Relative:
            if imgSize is None:
                raise IOError("Parameter 'imgSize' is required. It is necessary to inform the image size.")
        if bbType == BBType.Detected:
            if classConfidence is None:
                raise IOError("For bbType='Detection', it is necessary to inform the classConfidence value.")
        self._classConfidence = classConfidence
        self._bbType = bbType
        self._classId = classId
        self._format = format
        if typeCoordinates == CoordinatesType.Relative:
            self._x, self._y, self._w, self._h = convertToAbsoluteValues(imgSize, (x, y, w, h))
            self._width_img = imgSize[0]
            self._height_img = imgSize[1]
            if format == BBFormat.XYWH:
                self._x2 = self._w
                self._y2 = self._h
                self._w = self._x2 - self._x
                self._h = self._y2 - self._y
            else:
                raise IOError('For relative coordinates, the format must be XYWH (x,y,width,height)')
        else:
            self._x = x
            self._y = y
            if format == BBFormat.XYWH:
                self._w = w
                self._h = h
                self._x2 = self._x + self._w
                self._y2 = self._y + self._h
            else:
                self._x2 = w
                self._y2 = h
                self._w = self._x2 - self._x
                self._h = self._y2 - self._y
        if imgSize is None:
            self._width_img = None
            self._height_img = None
        else:
            self._width_img = imgSize[0]
            self._height_img = imgSize[1]

    def getAbsoluteBoundingBox(self, format=BBFormat.XYWH):
        if format == BBFormat.XYWH:
            return (
             self._x, self._y, self._w, self._h)
        if format == BBFormat.XYX2Y2:
            return (
             self._x, self._y, self._x2, self._y2)

    def getRelativeBoundingBox(self, imgSize=None):
        if imgSize is None:
            if self._width_img is None:
                if self._height_img is None:
                    raise IOError("Parameter 'imgSize' is required. It is necessary to inform the image size.")
        if imgSize is None:
            return convertToRelativeValues((imgSize[0], imgSize[1]), (
             self._x, self._y, self._w, self._h))
        return convertToRelativeValues((self._width_img, self._height_img), (
         self._x, self._y, self._w, self._h))

    def getImageName(self):
        return self._imageName

    def getConfidence(self):
        return self._classConfidence

    def getFormat(self):
        return self._format

    def getClassId(self):
        return self._classId

    def getImageSize(self):
        return (
         self._width_img, self._height_img)

    def getCoordinatesType(self):
        return self._typeCoordinates

    def getBBType(self):
        return self._bbType

    @staticmethod
    def compare(det1, det2):
        det1BB = det1.getAbsoluteBoundingBox()
        det1ImgSize = det1.getImageSize()
        det2BB = det2.getAbsoluteBoundingBox()
        det2ImgSize = det2.getImageSize()
        if det1.getClassId() == det2.getClassId():
            if det1.classConfidence == det2.classConfidenc():
                if det1BB[0] == det2BB[0]:
                    if det1BB[1] == det2BB[1]:
                        if det1BB[2] == det2BB[2]:
                            if det1BB[3] == det2BB[3]:
                                if det1ImgSize[0] == det1ImgSize[0]:
                                    if det2ImgSize[1] == det2ImgSize[1]:
                                        return True
        return False

    @staticmethod
    def clone(boundingBox):
        absBB = boundingBox.getAbsoluteBoundingBox(format=(BBFormat.XYWH))
        newBoundingBox = BoundingBox((boundingBox.getImageName()),
          (boundingBox.getClassId()),
          (absBB[0]),
          (absBB[1]),
          (absBB[2]),
          (absBB[3]),
          typeCoordinates=(boundingBox.getCoordinatesType()),
          imgSize=(boundingBox.getImageSize()),
          bbType=(boundingBox.getBBType()),
          classConfidence=(boundingBox.getConfidence()),
          format=(BBFormat.XYWH))
        return newBoundingBox
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sail_utils\cv\base.py
# Compiled at: 2020-04-07 01:46:40
# Size of source mod 2**32: 2281 bytes
"""
module for base class
"""
from abc import ABC, abstractmethod
from pathlib import Path
import cv2
from sail_utils import LOGGER

class _Streamer(ABC):

    def __init__(self, source: str, rate: int):
        self._source = Path(source)
        self._rate = rate
        self._stream = None

    @property
    def source(self):
        """
        get the source
        :return:
        """
        return self._source.as_posix()

    @property
    def rate(self):
        """
        get the sampling rate
        :return:
        """
        return self._rate

    @property
    def stream(self):
        """
        get the internal stream
        :return:
        """
        return self._stream


class _Detector(ABC):

    def __init__(self, server: str, src_size: int, dst_size: int, threshold: float, timeout: float):
        self._server = server
        self._threshold = threshold
        self._mapper = _Mapper(src_size, dst_size)
        self._timeout = timeout
        LOGGER.info(f"detector at: <{self._server}> with threshold <{self._threshold:.2f}>")

    @abstractmethod
    def detect(self, img, epoch) -> list:
        """
        method to detect a image
        :param img:
        :param epoch:
        :return:
        """
        pass

    def __str__(self):
        return f"mapper: {self._mapper}\nserver: {self._server}"


class _Mapper:

    def __init__(self, src: int, dst: int):
        self._src = src
        self._dst = dst
        LOGGER.info(f"mapper from <{self._src}> to <{self._dst}>")

    def resize(self, img):
        """
        resize pic to destination size
        :param img:
        :return:
        """
        return cv2.resize(img, (self._dst, self._dst), interpolation=(cv2.INTER_AREA))

    def __call__(self, bbox):
        scale = self._src / self._dst
        return [
         int(bbox[0] * scale),
         int(bbox[1] * scale),
         int(bbox[2] * scale),
         int(bbox[3] * scale)]

    def __str__(self):
        return f"source: <{self._src} - destination: <{self._dst}>"
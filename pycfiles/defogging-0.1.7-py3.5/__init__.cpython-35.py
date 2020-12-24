# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\defogging\__init__.py
# Compiled at: 2017-08-16 04:08:36
# Size of source mod 2**32: 2003 bytes
from PIL import Image
import numpy as np, sys
from .defogging import defogging

class Defog:

    def __init__(self):
        self._Defog__foggy_name = None
        self._Defog__foggy_img = None
        self._Defog__foggy_src = None
        self._Defog__defogged = None

    def read_img(self, name):
        """
        read a foggy image from hard disk

        :param name: the name of the foggy image
        """
        self._Defog__foggy_name = name
        self._Defog__foggy_img = Image.open(name)
        self._Defog__foggy_src = np.array(self._Defog__foggy_img).astype(float) / 255

    def read_array(self, array, range):
        """
        read a foggy object from numpy.array

        :param array: a foggy object in numpy.array
        :param range: the range of the input array, only in two value: 1 and 255
                      1 means array's range in [0,1], 255 means array's range in [0,255]
        """
        if range == 1:
            self._Defog__foggy_src = array.astype(float)
        elif range == 255:
            self._Defog__foggy_src = array.astype(float) / 255

    def defog(self):
        self._Defog__defogged = defogging(self._Defog__foggy_src)

    def get_array(self, range):
        """
        return the defogged array

        :param range: the range of the defogged array, only in two value: 1 and 255
                      1 means array's range in [0,1], 255 means array's range in [0,255]
        """
        if self._Defog__defogged == None:
            return 0
        if range == 1:
            return self._Defog__defogged
        if range == 255:
            return np.uint8(self._Defog__defogged * 255)

    def save_img(self, name):
        """
        save defogged image to the hard disk

        :param name: name of image
        """
        defogged_img = Image.fromarray(np.uint8(self._Defog__defogged * 255))
        defogged_img.save(name)


def main():
    args = sys.argv
    name = args[1]
    df = Defog()
    df.read_img(name)
    df.defog()
    df.save_img(name + '_defogged.bmp')


if __name__ == '__main__':
    main()
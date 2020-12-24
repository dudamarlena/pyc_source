# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xmind2Excel\file\xmind-sdk-python-master\xmind\core\position.py
# Compiled at: 2019-07-01 23:22:26
# Size of source mod 2**32: 839 bytes
"""
    xmind.core.position
    ~~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""
__author__ = 'aiqi@xmind.net <Woody Ai>'
from . import const
from .mixin import WorkbookMixinElement

class PositionElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_POSITION

    def __init__(self, node=None, ownerWorkbook=None):
        super(PositionElement, self).__init__(node, ownerWorkbook)

    def getX(self):
        return self.getAttribute(const.ATTR_X)

    def getY(self):
        return self.getAttribute(const.ATTR_Y)

    def setX(self, x):
        self.setAttribute(const.ATTR_X, int(x))

    def setY(self, y):
        self.setAttribute(const.ATTR_Y, int(y))


def main():
    pass


if __name__ == '__main__':
    main()
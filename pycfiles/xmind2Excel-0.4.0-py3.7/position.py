# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\workspace\test01\xmind2.0\xxmind\file\xmind-sdk-python-master\xmind\core\position.py
# Compiled at: 2018-11-13 07:00:38
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
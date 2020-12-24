# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\workspace\test01\xmind2.0\xxmind\file\xmind-sdk-python-master\xmind\core\title.py
# Compiled at: 2018-11-13 07:00:38
"""
    xmind.core.title
    ~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""
__author__ = 'aiqi@xmind.net <Woody Ai>'
from . import const
from .mixin import WorkbookMixinElement

class TitleElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_TITLE

    def __init__(self, node=None, ownerWorkbook=None):
        super(TitleElement, self).__init__(node, ownerWorkbook)


def main():
    pass


if __name__ == '__main__':
    main()
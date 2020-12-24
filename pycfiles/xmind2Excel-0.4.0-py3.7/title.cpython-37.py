# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xmind2Excel\file\xmind-sdk-python-master\xmind\core\title.py
# Compiled at: 2019-07-01 23:22:26
# Size of source mod 2**32: 488 bytes
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
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/data/core/meta.py
# Compiled at: 2019-07-27 12:37:23
# Size of source mod 2**32: 338 bytes
from abc import ABCMeta, abstractclassmethod
from icv.utils import EasyDict

class Meta(object):
    __metaclass__ = ABCMeta


class SampleMeta(EasyDict):

    def dict(self):
        return super(SampleMeta, self).dict()


class AnnoMeta(EasyDict):

    def dict(self):
        return super(AnnoMeta, self).dict()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/miscprom/core/util.py
# Compiled at: 2018-05-23 09:05:43
# Size of source mod 2**32: 169 bytes
from django.shortcuts import get_object_or_404
from miscprom.core.models import ApiKey

class Collector(object):

    def __init__(self, view):
        self.view = view
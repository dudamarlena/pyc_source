# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fxg2svg/processors/stroke.py
# Compiled at: 2016-06-27 19:20:12
# Size of source mod 2**32: 880 bytes
from lxml import etree
from .default import DefaultTagProcessor
processors = {}

def tag_processor(tagname):

    def register_tag_processor(cls):
        processors[tagname] = cls()
        return cls

    return register_tag_processor


@tag_processor('SolidColorStroke')
class SolidColorStrokeTagProcessor(DefaultTagProcessor):

    def on_start(self, target):
        color = target.attrs.get('color', '#000000')
        target.element.set('stroke', color)
        strokewidth = target.attrs.get('weight')
        if strokewidth:
            target.element.set('stroke-width', strokewidth)
        strokemiterlimit = target.attrs.get('miterLimit')
        if strokemiterlimit:
            target.element.set('stroke-miterlimit', strokemiterlimit)

    def on_end(self, target):
        pass
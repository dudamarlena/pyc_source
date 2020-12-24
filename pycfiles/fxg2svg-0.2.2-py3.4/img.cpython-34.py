# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fxg2svg/processors/img.py
# Compiled at: 2016-07-12 14:57:51
# Size of source mod 2**32: 1478 bytes
from lxml import etree
from PIL import Image
import uuid, base64
from io import BytesIO
from ..utils import process_transform
from .default import DefaultTagProcessor
from .common import NAMESPACEMAP
processors = {}

def tag_processor(tagname):

    def register_tag_processor(cls):
        processors[tagname] = cls()
        return cls

    return register_tag_processor


@tag_processor('BitmapImage')
class BitmapImageTagProcessor(DefaultTagProcessor):

    def on_start(self, target):
        params = {}
        params.update(process_transform(**target.attrs))
        if 'source' in target.attrs:
            src = target.attrs['source']
            if src.startswith('@Embed'):
                src = src[src.find('(') + 2:src.find(')') - 1]
                params['width'], params['height'] = map(lambda s: '%s' % s, Image.open(src).size)
            params['{%s}href' % NAMESPACEMAP['xlink']] = src
        if 'width' in target.attrs:
            params['width'] = target.attrs['width']
        if 'height' in target.attrs:
            params['height'] = target.attrs['height']
        target.element = etree.SubElement(target.element, 'image', **params)
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fxg2svg/processors/mask.py
# Compiled at: 2016-07-12 14:57:57
# Size of source mod 2**32: 982 bytes
from lxml import etree
import uuid
from ..utils import process_transform
from .default import DefaultTagProcessor
processors = {}

def tag_processor(tagname):

    def register_tag_processor(cls):
        processors[tagname] = cls()
        return cls

    return register_tag_processor


def remove_group_elements(element, tag):
    for e in element:
        if tag == e.tag:
            for ch in e:
                remove_group_elements(ch, tag)
                element.append(ch)

            element.remove(e)
            continue


@tag_processor('mask')
class MaskTagProcessor(DefaultTagProcessor):

    def on_start(self, target):
        params = {}
        params['id'] = str(uuid.uuid4())
        target.element = etree.SubElement(target.element, 'clipPath', **params)

    def on_end(self, target):
        remove_group_elements(target.element, 'g')
        super(MaskTagProcessor, self).on_end(target)
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fxg2svg/processors/default.py
# Compiled at: 2016-07-14 12:54:06
# Size of source mod 2**32: 473 bytes
from lxml import etree
import logging
logger = logging.getLogger(__name__)

class DefaultTagProcessor(object):

    def on_start(self, target):
        target.element = etree.SubElement(target.element, 'foreignObject')

    def on_end(self, target):
        parent = target.element.getparent()
        if parent is not None:
            target.element = parent

    def on_data(self, target):
        target.element.text = target.text
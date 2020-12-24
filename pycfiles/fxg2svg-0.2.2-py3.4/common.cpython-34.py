# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fxg2svg/processors/common.py
# Compiled at: 2016-07-14 12:56:10
# Size of source mod 2**32: 2788 bytes
from lxml import etree
import logging
from ..utils import process_transform, populate_transform
from .default import DefaultTagProcessor
logger = logging.getLogger(__name__)
NAMESPACEMAP = {None: 'http://www.w3.org/2000/svg', 
 'xlink': 'http://www.w3.org/1999/xlink'}
processors = {}

def tag_processor(tagname):

    def register_tag_processor(cls):
        processors[tagname] = cls()
        return cls

    return register_tag_processor


@tag_processor('Graphic')
class GraphicTagProcessor(DefaultTagProcessor):

    def on_start(self, target):
        attrs = target.attrs
        target.element = etree.Element('svg', nsmap=NAMESPACEMAP, version='1.1', width=attrs.get('viewWidth'), height=attrs.get('viewHeight'), viewBox=('0 0 %s %s' % (attrs.get('viewWidth'), attrs.get('viewHeight'))), preserveAspectRatio='none', **{'enable-background': 'new 0 0 %s %s' % (attrs.get('viewWidth'), attrs.get('viewHeight'))})


@tag_processor('Library')
class LibraryTagProcessor(DefaultTagProcessor):

    def on_start(self, target):
        root = target.root
        target.element = etree.SubElement(root, 'defs')


@tag_processor('Group')
class GroupTagProcessor(DefaultTagProcessor):

    def on_start(self, target):
        params = {}
        params.update(process_transform(**target.attrs))
        if 'alpha' in target.attrs:
            params['opacity'] = target.attrs['alpha']
        target.element = etree.SubElement(target.element, 'g', **params)

    def on_end(self, target):
        if 'transform' in target.element.attrib:
            populate_transform(target.element)
        element = target.element
        self.process_children(element)
        parent = element.getparent()
        target.element = parent

    def process_children(self, element):
        logger.debug('Process chidlren %s' % element.tag)
        clippathid = None
        maskedElements = []
        for e in element:
            logger.debug('chidlren %s' % e.tag)
            if clippathid:
                if e.tag == 'g':
                    g = e
                    g.attrib['clip-path'] = 'url(#%s)' % clippathid
                else:
                    g = etree.Element('g', **{'clip-path': 'url(#%s)' % clippathid})
                    g.append(e)
                maskedElements.append(g)
            if e.tag == 'clipPath':
                clippathid = e.attrib['id']
                continue

        logger.debug(maskedElements)
        for e in maskedElements:
            element.append(e)
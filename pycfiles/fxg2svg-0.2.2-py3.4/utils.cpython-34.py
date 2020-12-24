# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fxg2svg/processors/utils.py
# Compiled at: 2016-06-28 18:54:41
# Size of source mod 2**32: 1361 bytes
import logging
logger = logging.getLogger(__name__)

def process_transform(**attrs):
    transform = []
    if 'x' in attrs or 'y' in attrs:
        x = float(attrs.get('x', 0))
        y = float(attrs.get('y', 0))
        transform.append('translate(%s,%s)' % (x, y))
    if 'scaleX' in attrs or 'scaleY' in attrs:
        transform.append('scale(%s,%s)' % (
         float(attrs.get('scaleX', '1')),
         float(attrs.get('scaleY', '1'))))
    if 'rotation' in attrs:
        transform.append('rotate(%s)' % attrs['rotation'])
    if len(transform) > 0:
        return {'transform': ' '.join(transform)}
    return {}


def get_attribute(element, attrname):
    if element is None:
        return
    if attrname in element.attrib:
        return element.attrib[attrname]
    return get_attribute(element.getparent(), attrname)


def populate_transform(element):
    for ch in element:
        if 'transform' in ch.attrib:
            ch.set('transform', '%s %s' % (element.attrib['transform'], ch.attrib['transform']))
        else:
            ch.set('transform', element.attrib['transform'])
        if ch.tag in ('clipPath', 'g'):
            populate_transform(ch)
            continue

    del element.attrib['transform']
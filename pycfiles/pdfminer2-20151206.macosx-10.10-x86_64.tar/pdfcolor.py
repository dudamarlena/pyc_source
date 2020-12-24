# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Projects/chris/various/pdfminer/venv/lib/python2.7/site-packages/pdfminer/pdfcolor.py
# Compiled at: 2015-10-31 16:12:15
from .psparser import LIT
import six
LITERAL_DEVICE_GRAY = LIT('DeviceGray')
LITERAL_DEVICE_RGB = LIT('DeviceRGB')
LITERAL_DEVICE_CMYK = LIT('DeviceCMYK')

class PDFColorSpace(object):

    def __init__(self, name, ncomponents):
        self.name = name
        self.ncomponents = ncomponents

    def __repr__(self):
        return '<PDFColorSpace: %s, ncomponents=%d>' % (self.name, self.ncomponents)


PREDEFINED_COLORSPACE = {}
for name, n in six.iteritems({'CalRGB': 3, 
   'CalGray': 1, 
   'Lab': 3, 
   'DeviceRGB': 3, 
   'DeviceCMYK': 4, 
   'DeviceGray': 1, 
   'Separation': 1, 
   'Indexed': 1, 
   'Pattern': 1}):
    PREDEFINED_COLORSPACE[name] = PDFColorSpace(name, n)
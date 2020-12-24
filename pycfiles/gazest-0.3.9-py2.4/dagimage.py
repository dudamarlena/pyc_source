# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/controllers/dagimage.py
# Compiled at: 2007-09-26 14:43:59
import logging
from gazest.lib.base import *
log = logging.getLogger(__name__)
import Image
from ImageDraw import Draw
from StringIO import StringIO

class DagimageController(BaseController):
    __module__ = __name__

    def arc(self, top, mid, bottom):
        """ Arcs top and bottom sections are ORable bit fields:
          1: lower node is left
          2: vertical
          4: lower node is right
        Middle section is boolean."""
        col = (111, 121, 125)
        (top, mid, bottom) = map(int, [top, mid, bottom])
        response.headers['Content-Type'] = 'image/png'
        img = Image.new('RGB', (24, 24), color=(255, 255, 255))
        draw = Draw(img)
        for i in range(3):
            mask = 2 ** i
            if mask & top:
                draw.line(((12, 0), (12 * i, 12)), fill=col)
                draw.line(((12 * i, 12), (12, 0)), fill=col)
            if mask & bottom:
                draw.line(((12, 24), (12 * (2 - i), 12)), fill=col)
                draw.line(((12 * (2 - i), 12), (12, 24)), fill=col)

        if mid:
            draw.line(((0, 12), (24, 12)), fill=col)
        sio = StringIO()
        img.save(sio, 'PNG')
        return sio.getvalue()

    def node(self, top, bottom):
        col = (111, 121, 125)
        (top, bottom) = map(int, [top, bottom])
        response.headers['Content-Type'] = 'image/png'
        img = Image.new('RGB', (24, 24), color=(255, 255, 255))
        draw = Draw(img)
        draw.rectangle(((6, 6), (18, 18)), fill=col)
        if top:
            draw.line(((12, 0), (12, 12)), fill=col)
        if bottom:
            draw.line(((12, 12), (12, 24)), fill=col)
        sio = StringIO()
        img.save(sio, 'PNG')
        return sio.getvalue()
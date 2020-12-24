# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/iframe.py
# Compiled at: 2019-05-31 13:49:51
# Size of source mod 2**32: 1638 bytes
"""
Beampy module to include iframe in svg using svg ForeignObject
"""
import beampy.document as document
from beampy.functions import gcs
from beampy.modules.core import beampy_module
import logging
_log = logging.getLogger(__name__)

class iframe(beampy_module):
    __doc__ = '\n    Include iframe in Beampy.\n\n    '

    def __init__(self, iframe_content, **kwargs):
        self.type = 'svg'
        self.load_args(kwargs)
        self.content = iframe_content
        if self.width is None:
            self.width = document._slides[gcs()].curwidth
            _log.info('Set the width to curwidth: %s' % self.width)
        if self.height is None:
            self.height = document._slides[gcs()].curheight
            _log.info('Set the height to curheight: %s' % self.height)
        self.register()

    def render(self):
        """
        Render the iframe as an svg ForeignObject
        """
        svgout = '<foreignObject x="0" y="0" width="{width}" height="{width}">\n        <div xmlns="http://www.w3.org/1999/xhtml">\n        <iframe src="{source}" style="width:{width}px;height:{height}px"></iframe>\n        </div></foreignObject>'
        svgout = svgout.format(width=(self.positionner.width), height=(self.positionner.height),
          source=(self.content))
        self.update_size(self.positionner.width, self.positionner.height)
        self.svgout = svgout
        self.rendered = True
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/control/draw.py
# Compiled at: 2018-11-22 01:29:12
# Size of source mod 2**32: 2030 bytes
from .control import Control
from ..layer.featuregroup import FeatureGroup
DEFAULT_POSITION = 'topleft'
DEFAULT_CIRCLE = False
DEFAULT_RECTANGLE = False

class Draw(Control):

    def __init__(self, options={}, handleFeatureGroup=True):
        super().__init__()
        self.options = options
        self.handleFeatureGroup = handleFeatureGroup
        self.featureGroup = None
        self._handleOptions()
        self._initJs()
        if handleFeatureGroup:
            self.addedToMap.connect(self.addDrawnToFeatureGroup)

    def _initJs(self):
        jsObject = 'new L.Control.Draw('
        if self.options:
            jsObject += '{options}'.format(options=(self._stringifyForJs(self.options)))
        jsObject += ')'
        self._createJsObject(jsObject)

    def _handleOptions(self):
        self.options['position'] = self.options.get('position', DEFAULT_POSITION)
        draw = self.options.get('draw', {})
        if draw is not False:
            draw['circle'] = draw.get('circle', DEFAULT_CIRCLE)
            draw['rectangle'] = draw.get('rectangle', DEFAULT_RECTANGLE)
            self.options['draw'] = draw
        edit = self.options.get('edit', {})
        if edit is not False:
            featureGroup = edit.get('featureGroup', None)
            if featureGroup is None:
                if self.handleFeatureGroup:
                    featureGroup = FeatureGroup()
                    edit['featureGroup'] = featureGroup
            self.featureGroup = featureGroup
            self.options['edit'] = edit

    def addDrawnToFeatureGroup(self):
        self.map.addLayer(self.featureGroup)
        self.map.drawCreated.connect(self.featureGroup.createAndAddDrawnLayer)
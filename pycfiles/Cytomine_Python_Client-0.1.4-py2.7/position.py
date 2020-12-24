# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cytomine/models/position.py
# Compiled at: 2017-09-05 05:52:58
__author__ = 'Marée Raphaël <raphael.maree@ulg.ac.be>'
__copyright__ = 'Copyright 2010-2017 University of Liège, Belgium, http://www.cytomine.be/'
from model import Model
from collection import Collection

class Position(Model):

    def __init__(self, params=None):
        super(Position, self).__init__(params)
        self._callback_identifier = 'position'

    def to_url(self):
        if hasattr(self, 'id'):
            return 'position/%d.json' % self.id
        else:
            return 'position.json'


class PositionCollection(Collection):

    def __init__(self, params=None):
        super(PositionCollection, self).__init__(Position, params)

    def to_url(self):
        if hasattr(self, 'imageinstance'):
            return 'imageinstance/' + str(self.imageinstance) + '/positions.json'
        else:
            return 'imageinstance.json'
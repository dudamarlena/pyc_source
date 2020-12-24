# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cytomine/models/model.py
# Compiled at: 2017-09-05 05:52:58
__author__ = 'Stévens Benjamin <b.stevens@ulg.ac.be>'
__contributors__ = ['Marée Raphaël <raphael.maree@ulg.ac.be>', 'Rollus Loïc <lrollus@ulg.ac.be']
__copyright__ = 'Copyright 2010-2015 University of Liège, Belgium, http://www.cytomine.be/'
import json

class Model(object):

    def __init__(self, params=None):
        if params:
            self.parse(params)

    def parse(self, params=None):
        obj = json.loads(params)
        self.__dict__ = obj

    def to_json(self):
        return json.dumps(self.__dict__)

    def to_url(self):
        raise NotImplementedError('Please Implement to_url method in %s' % self.__class__.__name__)

    def is_new(self):
        return not hasattr(self, 'id')
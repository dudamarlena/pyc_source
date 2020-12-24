# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cytomine/models/storage.py
# Compiled at: 2017-09-05 05:52:58
__author__ = 'Stévens Benjamin <b.stevens@ulg.ac.be>'
__contributors__ = ['Marée Raphaël <raphael.maree@ulg.ac.be>', 'Rollus Loïc <lrollus@ulg.ac.be']
__copyright__ = 'Copyright 2010-2015 University of Liège, Belgium, http://www.cytomine.be/'
from model import Model
from collection import Collection

class Storage(Model):

    def __init__(self, params=None):
        super(Storage, self).__init__(params)
        self._callback_identifier = 'storage'

    def to_url(self):
        if hasattr(self, 'id'):
            return 'storage/%d.json' % self.id
        else:
            return 'storage.json'

    def __str__(self):
        return str(self.id) + ' : ' + str(self.name)


class UploadedFile(Model):

    def __init__(self, params=None):
        super(UploadedFile, self).__init__(params)
        self._callback_identifier = 'uploadedfile'

    def to_url(self):
        if hasattr(self, 'id'):
            return 'uploadedfile/%d.json' % self.id
        else:
            return 'uploadedfile.json'

    def __str__(self):
        return 'Uploadedfile : ' + str(self.id)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/identity.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 1620 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
try:
    import logging
    from models.base.base_object import BaseObject
except Exception as e:
    logging.exception(e)

class Identity(BaseObject):
    __doc__ = 'Identity class \n    '

    def __init__(self, account, json_object=None, url=None):
        """
        Constructor
        """
        super().__init__(account, json_object, url)

    def community(self):
        if self.json_object == None:
            if self.url != None:
                self.json_object = self.get_json(self.url)
                return self.json_object.get('community', '')
        else:
            return self.json_object.get('community', '')

    def text(self):
        if self.json_object == None:
            if self.url != None:
                self.json_object = self.get_json(self.url)
                return self.json_object.get('text', '')
        else:
            return self.json_object.get('text', '')

    def created(self):
        if self.json_object == None:
            if self.url != None:
                self.json_object = self.get_json(self.url)
                return self.json_object.get('created', '')
        else:
            return self.json_object.get('created', '')

    def modified(self):
        if self.json_object == None:
            if self.url != None:
                self.json_object = self.get_json(self.url)
                return self.json_object.get('modified', '')
        else:
            return self.json_object.get('modified', '')
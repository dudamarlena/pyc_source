# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hstools/resource.py
# Compiled at: 2019-09-19 10:33:37
# Size of source mod 2**32: 400 bytes


class ResourceMetadata(object):

    def __init__(self, system_meta, science_meta):
        self.__dict__.update(science_meta)
        self.__dict__.update(system_meta)

    @property
    def url(self):
        return self.resource_url

    @property
    def abstract(self):
        return self.description

    @property
    def keywords(self):
        return [s['value'] for s in self.subjects]
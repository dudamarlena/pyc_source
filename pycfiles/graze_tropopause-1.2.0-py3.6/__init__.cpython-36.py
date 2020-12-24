# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tropopause/__init__.py
# Compiled at: 2018-02-02 11:23:12
# Size of source mod 2**32: 725 bytes
__version__ = '1.1.1'
from troposphere import Tags as upstreamTags

class Tags(upstreamTags):
    __doc__ = ' extended upstream to prevent tag duplication '

    def __init__(self, *args, **kwargs):
        (super(Tags, self).__init__)(*args, **kwargs)
        self.tags = self._dedupe(self.tags)

    def __add__(self, newtags):
        newtags.tags = self._dedupe(self.tags + newtags.tags)
        return newtags

    def _dedupe(self, tags):
        interim = {}
        result = []
        for tag in self.tags + tags:
            interim[tag['Key']] = tag['Value']

        for key, val in interim.items():
            result.append({'Key':key, 
             'Value':val})

        return result
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/NamedExternalResource.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.terminal.external_resource import ExternalResource

class NamedExternalResource(ExternalResource):

    def __init__(self, name, sourceURL):
        super(NamedExternalResource, self).__init__(sourceURL)
        self._name = name

    def getName(self):
        return self._name
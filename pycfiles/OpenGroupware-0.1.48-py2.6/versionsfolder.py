# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/versionsfolder.py
# Compiled at: 2012-10-12 07:02:39
import os
from coils.core import *
from coils.net import *
from bpmlobject import BPMLObject
from yamlobject import YAMLObject
from utility import route_versions, process_versions

class VersionsFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_PUT(self):
        return True

    def _load_contents(self):
        self.data = {}
        if isinstance(self.entity, Route):
            for edition in route_versions(self.entity):
                name = ('{0}.{1}.bpml').format(self.entity.name, edition)
                self.insert_child(name, BPMLObject(self, name, entity=self.entity, version=edition, context=self.context, request=self.request))

        elif isinstance(self.entity, Process):
            for edition in process_versions(self.entity):
                name = ('{0}.{1}.yaml').format(self.entity.object_id, edition)
                self.insert_child(name, YAMLObject(self, name, entity=self.entity, version=edition, context=self.context, request=self.request))

        else:
            return False
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if self.load_contents():
            if self.has_child(name):
                return self.get_child(name)
        raise self.no_such_path()
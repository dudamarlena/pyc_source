# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/formatsfolder.py
# Compiled at: 2012-10-12 07:02:39
import os, yaml
from tempfile import mkstemp
from coils.core import *
from coils.net import DAVFolder
from coils.logic.workflow import Format
from formatobject import FormatObject

class FormatsFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_PUT(self):
        return True

    def supports_DELETE(self):
        return True

    def _load_contents(self):
        self.data = {}
        if self.name == 'Formats':
            for name in Format.ListFormats():
                try:
                    format = Format.Load(name)
                except Exception, e:
                    pass
                else:
                    self.insert_child(('{0}.yaml').format(name), format)

        else:
            return False
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if self.load_contents():
            if self.has_child(name):
                return FormatObject(self, name, entity=self.get_child(name), context=self.context, request=self.request)
        self.no_such_path()

    def do_PUT(self, request_name):
        """ Allows formats to be created by dropping YAML documents into /dav/Workflow/Formats """
        try:
            payload = self.request.get_request_payload()
            format = self.context.run_command('format::new', yaml=payload)
        except Exception, e:
            self.log.exception(e)
            raise CoilsException('Format creation failed.')

        self.context.commit()
        if format.get_name() != request_name[:-5]:
            self.request.simple_response(301, headers={'Location': ('/dav/Workflow/Formats/{0}.yaml').format(format.get_name())})
        else:
            self.request.simple_response(201)

    def do_DELETE(self, name):
        if name.endswith('.yaml'):
            name = name[:-5]
        if Format.Delete(name):
            self.request.simple_response(204)
        else:
            self.no_such_path()
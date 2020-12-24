# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/xsdfolder.py
# Compiled at: 2012-10-12 07:02:39
import json
from coils.core import *
from coils.net import DAVFolder, StaticObject
from xsdobject import XSDObject
from coils.logic.workflow import XSDDocument

class XSDFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_PUT(self):
        return True

    def _load_contents(self):
        for name in XSDDocument.List():
            try:
                xsd = XSDDocument.Marshall(name)
            except Exception, e:
                pass
            else:
                self.insert_child(name, XSDObject(self, name, entity=xsd, context=self.context, request=self.request))

        return True

    def do_PUT(self, request_name):
        """ Allows tables to be created by dropping YAML documents into /dav/Workflow/Tables """
        payload = self.request.get_request_payload()
        xsd = XSDDocument.Marshall(request_name)
        xsd.fill(data=payload)
        xsd.close()
        self.context.commit()
        self.request.simple_response(201)

    def do_DELETE(self, request_name):
        if self.load_contents():
            if self.has_child(request_name):
                xsd = self.get_child(request_name)
                xsd.entity.delete()
                self.request.simple_response(204, data=None, mimetype='application/xml', headers={})
                return
            self.no_such_path()
        else:
            raise CoilsException('Unable to enumerate collection contents.')
        return
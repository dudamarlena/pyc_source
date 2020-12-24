# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/wsdlfolder.py
# Compiled at: 2012-10-12 07:02:39
import json
from coils.core import *
from coils.net import DAVFolder, StaticObject
from wsdlobject import WSDLObject
from coils.logic.workflow import WSDLDocument

class WSDLFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_PUT(self):
        return True

    def _load_contents(self):
        for name in WSDLDocument.List():
            print name
            try:
                xsd = WSDLDocument.Marshall(name)
            except Exception, e:
                pass
            else:
                self.insert_child(name, WSDLObject(self, name, entity=xsd, context=self.context, request=self.request))

        return True

    def do_PUT(self, request_name):
        """ Allows tables to be created by dropping YAML documents into /dav/Workflow/Tables """
        try:
            payload = self.request.get_request_payload()
            wsdl = WSDLDocument.Marshall(request_name)
            wsdl.fill(data=payload)
            wsdl.close()
        except Exception, e:
            self.log.exception(e)
            raise CoilsException('XSD Object Creation Failed.')

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
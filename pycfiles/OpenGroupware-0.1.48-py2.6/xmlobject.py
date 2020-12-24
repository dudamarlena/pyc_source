# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/xmlobject.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import BLOBManager
from coils.core import CoilsException
from lxml import etree

class XMLDocument(object):
    __handle__ = None

    def __init__(self, name):
        self.name = name

    @property
    def filename(self):
        return ('wf/{0}/{1}').format(self.__container__, self.name)

    @property
    def size(self):
        return BLOBManager.SizeOf(self.filename)

    @property
    def created(self):
        return BLOBManager.Created(self.filename)

    @property
    def modified(self):
        return BLOBManager.Modified(self.filename)

    @property
    def handle(self):
        if not self.__handle__:
            self.__handle__ = BLOBManager.Open(self.filename, 'r+', encoding='binary', create=True)
        return self.__handle__

    @property
    def read_handle(self):
        return BLOBManager.Open(self.filename, 'r', encoding='binary')

    def close(self):
        if self.__handle__:
            BLOBManager.Close(self.__handle__)
        self.__handle__ = None
        return

    def delete(self):
        self.close()
        BLOBManager.Delete(self.filename)

    def verify(self, rfile=None, data=None):
        pass

    def fill(self, rfile=None, data=None):
        self.verify(rfile=rfile, data=data)
        wfile = self.handle
        wfile.truncate()
        if rfile:
            rfile.seek(0)
            shutil.copyfileobj(rfile, wfile)
        else:
            wfile.write(data)
        wfile.flush()

    def rewind(self):
        self.__handle__.seek(0)


class XSDDocument(XMLDocument):
    __container__ = 'x'

    def verify(self, rfile=None, data=None):
        try:
            if rfile:
                xsd_doc = etree.parse(rfile)
            else:
                xsd_doc = etree.fromstring(data)
            etree.XMLSchema(xsd_doc)
        except Exception, e:
            raise e

    def __repr__(self):
        return ('<XSDDocument name="{0}" path="{1}"/>').format(self.name, self.filename)

    @staticmethod
    def Marshall(name):
        return XSDDocument(name)

    @staticmethod
    def List():
        result = []
        for name in BLOBManager.List(('wf/{0}/').format(XSDDocument.__container__)):
            result.append(name)

        return result


class WSDLDocument(XMLDocument):
    __container__ = 'w'

    @staticmethod
    def Marshall(name):
        return WSDLDocument(name)

    @staticmethod
    def List():
        result = []
        for name in BLOBManager.List(('wf/{0}/').format(WSDLDocument.__container__)):
            result.append(name)

        return result


class XSLTDocument(XMLDocument):
    __container__ = 'xslt'

    def verify(self, rfile=None, data=None):
        try:
            if rfile:
                xsd_doc = etree.parse(rfile)
            else:
                xsd_doc = etree.fromstring(data)
            etree.XSLT(xsd_doc)
        except Exception, e:
            raise e

    @staticmethod
    def Marshall(name):
        return XSLTDocument(name)

    @staticmethod
    def List():
        result = []
        for name in BLOBManager.List(('wf/{0}/').format(XSLTDocument.__container__)):
            result.append(name)

        return result
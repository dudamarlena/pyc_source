# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/spectools/interface2OM.py
# Compiled at: 2008-10-01 10:40:59
import os
from lxml import etree
from commonOM import Descr
from interfaceOM import Event
from interfaceOM import Request
from interfaceOM import Reply
from interfaceOM import Interface
from interfacens2OM import loadInterfacens
from structns2OM import loadStructns

def getStructNamespace(classDir, relPath=''):
    p = os.path.join(classDir, relPath, 'structns.xml')
    s = loadStructns(p)
    if s.ns.has_key('xml'):
        return s.ns['xml'].package
    else:
        return
    return


class NotInterfaceException(Exception):
    __module__ = __name__

    def __init__(self, filename='<unknown>'):
        filename = filename

    def __repr__(self):
        return '%s is not an interface instance' % self.filename

    def __str__(self):
        return __repr__()


def loadInterface(filename):
    path = os.path.normcase(os.path.abspath(filename))
    if not os.path.exists(path):
        raise NotInterfaceException(filename=filename)
    interfaceDir = os.path.dirname(path)
    interface = None
    interfaceFileName = path
    is_first_elem = True
    curElem = None
    curObject = None
    inEvent = 0
    inExtends = 0
    for (event, elem) in etree.iterparse(path, events=('start', 'end'), attribute_defaults=True):
        name = elem.tag
        if event == 'start':
            if is_first_elem and name != 'interface':
                raise NotInterfaceException(filename=filename)
            else:
                is_first_elem = False
            if name == 'interface':
                interface = Interface(elem.attrib['name'])
                curObject = interface
                interface.specFile = interfaceFileName
                nsPath = os.path.join(interfaceDir, 'interfacens.xml')
                if os.path.exists(nsPath):
                    interface.interfaceNs = loadInterfacens(nsPath)
            elif name == 'event':
                curEvent = Event()
                curObject = curEvent
                inEvent = 1
                curEvent.name = elem.attrib['name']
                curEvent.visibility = elem.attrib['visibility']
                curEvent.isInstanceMethod = True
                if elem.attrib.has_key('special'):
                    curEvent.special = elem.attrib['special']
                interface.methods.append(curEvent)
            elif name == 'rqst' or name == 'rply':
                o = None
                if name == 'rqst':
                    o = Request()
                    curObject = o
                    curEvent.rqst = o
                else:
                    o = Reply()
                    curObject = o
                    curEvent.rply = o
                o.className = (
                 getStructNamespace(interfaceDir, elem.attrib['classpath']), elem.attrib['class'])
                if elem.attrib['classpath'] is not None:
                    o.classPath = os.path.join(os.path.abspath(interfaceDir), elem.attrib['classpath'])
                o.isList = elem.attrib['list'] == 'y'
                o.isOptional = elem.attrib['optional'] == 'y'
                o.isValidated = elem.attrib['validated'] == 'y'
            elif name == 'extends':
                inExtends = 1
                interface.extends.append(loadInterface(os.path.join(interfaceDir, elem.attrib['interfacepath'], elem.attrib['interface'] + '.xml')))
        elif event == 'end':
            if name == 'descr':
                descr = Descr()
                descr.language = elem.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)
                descr.description = elem.text
                if inEvent:
                    curEvent.descr.append(descr)
                else:
                    interface.descr.append(descr)
            elif name == 'event':
                inEvent = 0
            elif name == 'extends':
                inExtends = 0
            elif name == 'doc':
                curObject.doc.append(etree.tostring(elem))

    return interface
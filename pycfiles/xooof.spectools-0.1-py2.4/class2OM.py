# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/spectools/class2OM.py
# Compiled at: 2008-10-01 10:40:59
import os
from lxml import etree
from structns2OM import loadStructns
from classns2OM import loadClassns
from fsm2OM import loadFSM
from classOM import Klass
from commonOM import Descr
from interfaceOM import Event
from interfaceOM import Reply
from interfaceOM import Request
from interfaceOM import Interface
from interface2OM import loadInterface

class NotClassException(Exception):
    __module__ = __name__

    def __init__(self, filename='<unknown>'):
        filename = filename

    def __repr__(self):
        return '%s is not a class instance' % self.filename

    def __str__(self):
        return __repr__()


def getStructNamespace(classDir, relPath=''):
    p = os.path.join(classDir, relPath, 'structns.xml')
    s = loadStructns(p)
    if s.ns.has_key('xml'):
        return s.ns['xml'].package
    else:
        return
    return


def getClassNamespace(classDir, relPath=''):
    p = os.path.join(classDir, relPath, 'classns.xml')
    s = loadClassns(p)
    if s.ns.has_key('xml'):
        return s.ns['xml'].package
    else:
        return
    return


def loadClass(filename):
    path = os.path.normcase(os.path.abspath(filename))
    if not os.path.exists(path):
        raise NotClassException(filename=filename)
    classDir = os.path.dirname(path)
    is_first_elem = True
    klass = Klass()
    klass.specFile = path
    firstElem = 1
    inClassMethods = 0
    inKlass = 0
    inInstanceMethods = 0
    curEvent = None
    inEvent = 0
    for (event, elem) in etree.iterparse(path, events=('start', 'end'), attribute_defaults=True):
        name = elem.tag
        if event == 'start':
            if is_first_elem and name != 'class':
                raise NotClassException(filename=filename)
            else:
                is_first_elem = False
            if name == 'class':
                klass.name = (
                 getClassNamespace(classDir), elem.attrib['name'])
                klass.classNs = loadClassns(os.path.join(classDir, 'classns.xml'))
                inKlass = 1
            elif name == 'classmethods':
                inClassMethods = 1
            elif name == 'defaultinterface':
                klass.defaultinterface = Interface(name)
                inInstanceMethods = 1
            elif name == 'event':
                curEvent = Event()
                inEvent = 1
                curEvent.name = elem.attrib['name']
                curEvent.visibility = elem.attrib['visibility']
                elem.attrib.get('special', None)
                if inClassMethods:
                    curEvent.isInstanceMethod = 0
                    klass.classmethods.append(curEvent)
                elif inInstanceMethods:
                    curEvent.isInstanceMethod = 1
                    klass.defaultinterface.methods.append(curEvent)
            elif name == 'rqst' or name == 'rply':
                o = None
                if name == 'rqst':
                    o = Request()
                    curEvent.rqst = o
                else:
                    o = Reply()
                    curEvent.rply = o
                o.className = (
                 getStructNamespace(classDir, elem.attrib['classpath']), elem.attrib['class'])
                if elem.attrib['classpath'] is not None:
                    o.classPath = os.path.join(os.path.abspath(classDir), elem.attrib['classpath'])
                o.isList = elem.attrib['list'] == 'y'
                o.isOptional = elem.attrib['optional'] == 'y'
                o.isValidated = elem.attrib['validated'] == 'y'
            elif name == 'extends':
                inExtends = 1
                klass.defaultinterface.extends.append(loadInterface(os.path.join(classDir, elem.attrib['interfacepath'], elem.attrib['interface'] + '.xml')))
        elif event == 'end':
            if name == 'descr':
                descr = Descr()
                descr.language = elem.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)
                descr.description = elem.text
                if inEvent:
                    curEvent.descr.append(descr)
                else:
                    klass.descr.append(descr)
            elif name == 'class':
                inKlass = 0
            elif name == 'classmethods':
                inClassMethods = 0
            elif name == 'defaultinterface':
                inInstanceMethods = 0
            elif name == 'event':
                inEvent = 0
            elif name == 'extends':
                inExtends = 0
            elif name == 'doc':
                if inKlass:
                    klass.doc.append(etree.tostring(elem))
                elif inEvent:
                    curEvent.doc.append(etree.tostring(elem))

    klass.fsm = loadFSM(path)
    return klass


if __name__ == '__main__':
    c = loadClass('/home/sagblmi/projects/nexus/src/tabellio.officium/tabellio/officium/models/classes/Person.xml')
    print c
    print c.descr[0]
    print '----------classmethods----------'
    for event in c.classmethods:
        print event
        print event.rqst
        print event.rply

    print '----------instancemethods----------'
    for event in c.defaultinterface.methods:
        pass
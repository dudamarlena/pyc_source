# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/spectools/structns2OM.py
# Compiled at: 2008-10-01 10:40:59
import os
from lxml import etree
import structnsOM
from commonOM import Descr
structNsFiles = {}
structNamespaces = {}

class NotStructnsException(Exception):
    __module__ = __name__

    def __init__(self, filename='<unknown>'):
        self.filename = filename

    def __repr__(self):
        return '%s is not a structns instance' % self.filename

    def __str__(self):
        return self.__repr__()


def _loadStructns(stream):
    structns = structnsOM.Structns()
    is_first_elem = True
    for (event, elem) in etree.iterparse(stream, events=('start', 'end')):
        name = elem.tag
        if event == 'start':
            if is_first_elem and name != 'structns':
                raise NotStructnsException()
            else:
                is_first_elem = False
        elif name == 'descr':
            descr = Descr()
            descr.language = elem.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)
            descr.description = elem.text
            structns.descr.append(descr)
        elif name == 'ns':
            ns = structnsOM.Ns()
            ns.type = elem.attrib['type']
            ns.package = elem.text or None
            ns.manifest = elem.attrib.get('manifest', None)
            structns.ns[ns.type] = ns

    return structns


def loadStructns(filename):
    path = os.path.normcase(os.path.abspath(filename))
    try:
        return structNsFiles[path]
    except KeyError:
        if os.path.exists(path):
            stream = open(path, 'r')
            try:
                s = _loadStructns(path)
                structNsFiles[path] = s
                if s.ns.has_key('xml'):
                    structNamespaces[s.ns['xml']] = s
                else:
                    structNamespaces[None] = s
                return s
            finally:
                stream.close()
        else:
            s = structnsOM.Structns()
            structNsFiles[path] = s
            structNamespaces[None] = s
            return s

    return


if __name__ == '__main__':
    f = 'structns.xml'
    s = loadStructns(f)
    for ns in s.ns.values():
        print ns

    print s.descr[0]
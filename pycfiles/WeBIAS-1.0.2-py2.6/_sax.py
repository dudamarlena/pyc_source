# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/parsers/_sax.py
# Compiled at: 2015-04-13 16:10:46
"""Pure-Python SAX parser for xml_pickle"""
__author__ = 'Frank McIngvale (frankm@hiwaay.net)'
from xml.sax.expatreader import ExpatParser
from xml.sax.handler import ContentHandler, ErrorHandler
from xml.sax.xmlreader import InputSource
from gnosis.xml.pickle.util import obj_from_name, unpickle_function, get_class_from_name, unsafe_string, unsafe_content
from gnosis.util.introspect import attr_update
import gnosis.xml.pickle.ext as mutate
from gnosis.xml.pickle.parsers import _dom
from gnosis.xml.pickle.parsers._dom import TRUE_VALUE, FALSE_VALUE
from gnosis.util.XtoY import to_number
import sys, os, string
from types import *
from StringIO import StringIO
XMLPicklingError = 'gnosis.xml.pickle.XMLPicklingError'
XMLUnpicklingError = 'gnosis.xml.pickle.XMLUnpicklingError'
DEBUG = 0

def dbg(msg, force=0):
    if DEBUG or force:
        print msg


class _EmptyClass():
    pass


class xmlpickle_handler(ContentHandler):

    def __init__(self, paranoia=1):
        self.paranoia = paranoia

    def startDocument(self):
        self.elem_stk = []
        self.val_stk = []
        self.visited = {}
        self.nr_objs = 0
        self.content = ''

    def getobj(self):
        """return final object"""
        return self.val_stk[(-1)][2]

    def prstk(self, force=0):
        if DEBUG == 0 and not force:
            return
        print '**ELEM STACK**'
        for i in self.elem_stk:
            print str(i)

        print '**VALUE STACK**'
        for i in self.val_stk:
            print str(i)

    def save_obj_id(self, obj, elem):
        id = elem[4].get('id')
        if id:
            self.visited[id] = obj

    def pop_stateinfo(self):
        i = -1
        while self.val_stk[i][0] != 'STOP':
            if self.val_stk[i][0] == 'attr' and self.val_stk[i][1] == '__getstate__':
                info = self.val_stk.pop(i)[2]
                return info
            i -= 1

        return

    def pop_initargs(self):
        i = -1
        while self.val_stk[i][0] != 'STOP':
            if self.val_stk[i][0] == 'attr' and self.val_stk[i][1] == '__getinitargs__':
                info = self.val_stk.pop(i)[2]
                return info
            i -= 1

        return

    def unpickle_instance(self, elem):
        obj = elem[5]
        args = self.pop_initargs()
        if hasattr(obj, '__init__') and args is not None:
            apply(obj.__init__, args)
        state = self.pop_stateinfo()
        if state:
            if hasattr(obj, '__setstate__'):
                obj.__setstate__(state)
            else:
                attr_update(obj, state)
        else:
            while self.val_stk[(-1)][0] != 'STOP':
                e = self.val_stk.pop()
                setattr(obj, e[1], e[2])

            self.val_stk.pop()
            return obj

    def reduce(self, name, bodytext):
        dbg('ABOUT TO REDUCE %s' % name)
        self.prstk()
        elem = self.elem_stk.pop()
        refid = elem[4].get('refid')
        if refid:
            obj = self.visited[refid]
            self.val_stk.append((elem[0], elem[3], obj))
            dbg('<<<<<<<<<<<< REDUCED')
            self.prstk()
            self.nr_objs += 1
            return
        else:
            if elem[4].get('value'):
                valuetext = unsafe_string(elem[4].get('value'))
            else:
                valuetext = unsafe_content(bodytext)
            if name in ('attr', 'key', 'val', 'item'):
                family = elem[1]
                if family == 'atom':
                    dbg('** ATOM')
                    obj = valuetext
                elif family == 'none':
                    dbg('** NONE')
                    obj = None
                elif family == 'seq':
                    dbg('** SEQ')
                    obj = elem[5]
                    while self.val_stk[(-1)][0] != 'STOP':
                        obj.insert(0, self.val_stk.pop()[2])

                    self.val_stk.pop()
                elif family == 'map':
                    dbg('** MAP')
                    obj = elem[5]
                    while self.val_stk[(-1)][0] != 'STOP':
                        e = self.val_stk.pop()
                        obj[e[2][0]] = e[2][1]

                    self.val_stk.pop()
                elif family == 'obj':
                    dbg('** OBJ')
                    obj = self.unpickle_instance(elem)
                elif family == 'lang':
                    if elem[2] == 'function':
                        obj = unpickle_function(elem[4].get('module'), elem[4].get('class'), self.paranoia)
                    elif elem[2] == 'class':
                        obj = get_class_from_name(elem[4].get('class'), elem[4].get('module'), self.paranoia)
                    else:
                        raise XMLUnpicklingError, 'Unknown lang type %s' % elem[2]
                elif family == 'uniq':
                    if elem[2] == 'function':
                        obj = unpickle_function(elem[4].get('module'), elem[4].get('class'), self.paranoia)
                    elif elem[2] == 'class':
                        obj = get_class_from_name(elem[4].get('class'), elem[4].get('module'), self.paranoia)
                    elif elem[2] == 'True':
                        obj = TRUE_VALUE
                    elif elem[2] == 'False':
                        obj = FALSE_VALUE
                    else:
                        raise XMLUnpicklingError, 'Unknown uniq type %s' % elem[2]
                else:
                    raise XMLUnpicklingError, 'UNKNOWN family %s,%s,%s' % (
                     family, elem[2], elem[3])
                if elem[2] == 'numeric':
                    dbg('** NUMERIC')
                    obj = to_number(obj)
                elif elem[2] == 'string':
                    dbg('** STRING')
                    obj = obj
                elif elem[2] == 'None':
                    obj = obj
                elif elem[2] in ('tuple', 'list'):
                    dbg('** TUPLE/LIST')
                    if elem[2] != 'list':
                        obj = tuple(obj)
                    else:
                        obj = obj
                elif elem[2] == 'dict':
                    obj = obj
                elif elem[2] == 'PyObject':
                    obj = obj
                elif elem[2] == 'function':
                    obj = obj
                elif elem[2] == 'class':
                    obj = obj
                elif elem[2] == 'True':
                    obj = obj
                elif elem[2] == 'False':
                    obj = obj
                elif mutate.can_unmutate(elem[2], obj):
                    mextra = elem[4].get('extra')
                    obj = mutate.unmutate(elem[2], obj, self.paranoia, mextra)
                else:
                    self.prstk(1)
                    raise XMLUnpicklingError, 'UNHANDLED elem %s' % elem[2]
                self.val_stk.append((elem[0], elem[3], obj))
                self.save_obj_id(obj, elem)
                self.nr_objs += 1
            elif name == 'entry':
                e1 = self.val_stk.pop()
                e2 = self.val_stk.pop()
                if e1[0] == 'val':
                    ent = (
                     elem[0], elem[3], (e2[2], e1[2]))
                else:
                    ent = (
                     elem[0], elem[3], (e1[2], e2[2]))
                self.save_obj_id(ent, elem)
                self.val_stk.append(ent)
            elif name == 'PyObject':
                obj = self.unpickle_instance(elem)
                if elem[2] is not None and len(elem[2]):
                    if mutate.can_unmutate(elem[2], obj):
                        obj = mutate.unmutate(elem[2], obj, self.paranoia, None)
                self.val_stk.append((elem[0], elem[3], obj))
                self.save_obj_id(obj, elem)
                self.nr_objs += 1
            else:
                raise str('UNHANDLED name %s' % name)
            dbg('<<<<<<<<<<<< REDUCED')
            self.prstk()
            return

    def endDocument(self):
        if DEBUG == 1:
            print 'NROBJS ' + str(self.nr_objs)

    def startElement(self, name, attrs):
        dbg('** START ELEM %s,%s' % (name, attrs._attrs))
        node_type = attrs._attrs.get('type')
        family = attrs._attrs.get('family')
        if node_type is None:
            if name == 'PyObject':
                family = 'obj'
            elif name == 'entry':
                family = ''
            else:
                family = _dom._fix_family(family, node_type)
            if attrs._attrs.get('refid') or family == 'seq':
                container = []
            elif family == 'map':
                container = {}
            elif family == 'obj' or name == 'PyObject':
                container = obj_from_name(attrs._attrs.get('class'), attrs._attrs.get('module', None), self.paranoia)
            else:
                container = None
        else:
            container = None
        elem = (name, family, node_type, attrs._attrs.get('name'),
         attrs._attrs, container)
        if container is not None:
            self.save_obj_id(container, elem)
        self.elem_stk.append(elem)
        if container is not None:
            if not attrs._attrs.get('refid'):
                self.val_stk.append(('STOP', ))
        self.content = ''
        self.prstk()
        return

    def endElement(self, name):
        self.reduce(name, self.content)

    def characters(self, content):
        self.content += content

    def error(self, exception):
        print '** ERROR - dumping stacks'
        self.prstk(1)
        raise exception

    def fatalError(self, exception):
        print '** FATAL ERROR - dumping stacks'
        self.prstk(1)
        raise exception

    def warning(self, exception):
        print 'WARNING'
        raise exception

    def resolveEntity(self, publicId, systemId):
        inp = InputSource()
        inp.setByteStream(StringIO(''))
        return inp


def thing_from_sax(filehandle=None, paranoia=1):
    if DEBUG == 1:
        print '**** SAX PARSER ****'
    e = ExpatParser()
    m = xmlpickle_handler(paranoia)
    e.setContentHandler(m)
    e.setErrorHandler(m)
    e.setEntityResolver(m)
    if filehandle:
        e.parse(filehandle)
    else:
        raise 'Must pass a fileobj'
    return m.getobj()
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/spectools/fsm2OM.py
# Compiled at: 2008-10-01 10:40:59
import os
from lxml import etree
from fsmOM import FSM
from commonOM import Descr

class NotFsmException(Exception):
    __module__ = __name__

    def __init__(self, filename='<unknown>'):
        filename = filename

    def __repr__(self):
        return '%s is not a fsm instance' % self.filename

    def __str__(self):
        return __repr__()


class NoNStateException(Exception):
    __module__ = __name__

    def __init__(self, filename='<unknown>'):
        filename = filename

    def __repr__(self):
        return '%s has no NState defined as first child of fsm element' % self.filename

    def __str__(self):
        return __repr__()


def loadFSM(filename):
    path = os.path.normcase(os.path.abspath(filename))
    if not os.path.exists(path):
        raise NotFsmException(filename=filename)
    classDir = os.path.dirname(path)
    fsm = FSM()
    fsm.classSpecFile = filename
    firstElem = 1
    inFsm = False
    curState = None
    data = ''
    container = fsm
    parentContainerStack = []
    for (event, elem) in etree.iterparse(path, events=('start', 'end'), attribute_defaults=True):
        name = elem.tag
        if event == 'start':
            if name == 'fsm':
                inFsm = True
            if inFsm and name != 'fsm':
                if firstElem:
                    if name == 'nstate':
                        firstElem = 0
                        curState = container.addNState(elem.attrib['name'])
                    else:
                        raise NoNStateException(fsm.classSpecFile)
                elif name == 'mstate':
                    parentContainerStack.append(container)
                    curState = container.addMState()
                    container = curState
                elif name == 'state':
                    curState = container.addState(elem.attrib['name'])
                elif name == 'transition':
                    curState.addTransition(elem.attrib['event'], elem.attrib.get('nextstate', None), elem.attrib.get('impl', None))
        elif event == 'end':
            if inFsm:
                if name == 'descr':
                    descr = Descr()
                    descr.language = elem.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)
                    descr.description = elem.text
                    curState.descr.append(descr)
                if name == 'mstate':
                    container = parentContainerStack.pop()

    return fsm
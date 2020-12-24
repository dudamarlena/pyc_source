# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/headincludes/resourcelibrary.py
# Compiled at: 2010-03-12 11:12:03
from zope.component import getUtility
from interfaces import IHeadIncludeRegistration
library_info = {}

class LibraryInfo(object):

    def __init__(self):
        self.included = []
        self.required = []


def _required(required_list, req):
    if req not in required_list:
        required_list.append(req)
        for r in getRequired(req):
            _required(required_list, r)


def need(library_name):
    registrar = getUtility(IHeadIncludeRegistration)
    if registrar:
        myList = []
        try:
            _required(myList, library_name)
        except KeyError:
            raise RuntimeError('Unknown resource library: %s' % library_name)
        else:
            myList.reverse()
            for lib in myList:
                included = getIncluded(lib)
                for file_name in included:
                    url = '/@@/%s/%s' % (lib, file_name)
                    registrar.register(url)


def getRequired(name):
    return library_info[name].required


def getIncluded(name):
    return library_info[name].included


try:
    from zope.testing.cleanup import addCleanUp
except ImportError:
    pass
else:
    addCleanUp(lambda : library_info.clear())
    del addCleanUp
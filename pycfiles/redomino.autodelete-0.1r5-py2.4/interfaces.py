# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/autodelete/utils/interfaces.py
# Compiled at: 2008-03-07 11:25:21
from zope.interface import Interface
from zope.schema import Dict
from redomino.autodelete import autodeleteMessageFactory as _

class IAutoDelete(Interface):
    """ Autodelete utility interface"""
    __module__ = __name__

    def run_autodelete():
        """ Auto-deletes all objects expired (with autodelete actived and with delete_date < now) """
        pass


class IAutoDeleteQuery(Interface):
    """ Defines the catalog query for objects to be deleted """
    __module__ = __name__
    query = Dict(title=_('The query catalog for objects to be deleted'))
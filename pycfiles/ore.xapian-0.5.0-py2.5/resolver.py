# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/xapian/resolver.py
# Compiled at: 2008-09-11 20:29:58
"""
$Id: $
"""
from sqlalchemy import orm
from zope.dottedname.resolve import resolve

def getKeyAndTable(ob):
    mapper = orm.object_mapper(ob)
    primary_key = mapper.primary_key_from_instance(ob)
    return (primary_key, mapper.select_table.fullname)


def getClassName(ob):
    klass = object.__class__
    return '%s.%s' % (klass.__module__, klass.__name__)


class AlchemistResolver(object):
    """
    resolver for sqlalchemy mapped objects
    """

    def id(self, object):
        pass

    def resolve(self, id):
        pass


class SubversionResolver(object):
    """
    resolver for subversion nodes ( ore.svn )
    """

    def id(self, object):
        pass

    def resolve(self, id):
        pass
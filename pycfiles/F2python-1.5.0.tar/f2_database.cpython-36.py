# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thibault/Work/Recherche/F2/F2Python/F2/f2_database.py
# Compiled at: 2017-04-05 17:17:14
# Size of source mod 2**32: 1717 bytes
"""
F2 Database Interface
---------------------

Definition of class    F 2 _ D a t a b a s e , 

Th. Estier
version 1.2 - june 2005
   --
   written after the original Ada version from 1989-1990, Th. Estier, CUI Geneva.
"""
from . import f2_object, f2_class, OFF, F2_NULL
F2_Object = f2_object.F2_Object
theClass = f2_class.theClass

class F2_Database(F2_Object):
    __doc__ = 'an F2 oid of kernel class Database'

    def __getattr__(self, name):
        if name[0] == '_':
            if name in ('_klass', '_rank'):
                return self.__dict__[name]
            if name[1] == '_':
                raise AttributeError
        else:
            try:
                return theClass(name, self)
            except (AttributeError, f2_object.ClassDesignationError):
                return super().__getattr__(name)


def theDatabase(db_designator):
    """F2_Database maker: db_designator is a string (db.name)"""
    Database = theClass(OFF.className.find('Database')[0])
    attrDBName = Database._attribute_of('name', Database._rank)
    stateDBattr = Database.classStateAttribute._rank
    designatedDB = [d for d in OFF.db_root[attrDBName].find(db_designator) if OFF.db_root[stateDBattr][d] != F2_NULL]
    if len(designatedDB) == 0:
        raise AttributeError(db_designator)
    else:
        return F2_Database(Database._rank, designatedDB[0])


f2_object._RegisterPythonClass('Database', F2_Database)
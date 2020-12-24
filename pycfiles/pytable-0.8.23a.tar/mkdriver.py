# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/mk/mkdriver.py
# Compiled at: 2003-08-02 18:46:25
from pytable import dbdriver
import metakit
from basicproperty import common

class MkDriver(dbdriver.DBDriver):
    """Metakit database driver
        """
    __module__ = __name__
    defaultTableClass = common.ClassByNameProperty('defaultTableClass', 'Default DBTable sub-class to be used for this driver', defaultValue='pytable.mk.mktable.MkTable')

    def establishConnection(self, fullSpecifier):
        """Connect using the fully specified specifier

                fullSpecifier -- a specifier with all arguments unified
                        and ready to be connected.  This specifier should
                        include everything required to do the actual
                        connection (including passwords or the like).

                All sub-classes must override this method!
                """
        filename = fullSpecifier.dsn
        return metakit.storage(filename, 1)
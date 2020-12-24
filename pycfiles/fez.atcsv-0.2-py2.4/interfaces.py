# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fez/atcsv/interfaces.py
# Compiled at: 2009-01-27 14:12:13
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from fez.atcsv import atcsvMessageFactory as _

class ICSVImport(Interface):
    __module__ = __name__

    def do_import(portal_type, delimiter, file_path=None, fp=None):
        """
        Import the CSV
        
        delimiter - single-char delimiter to use
        
        file_path - path on the filesystem to load
        
        fp - file-like object to load
        
        You should specify either fp or file_path. Behaviour is 
        undefined if you specify both.        
        """
        pass
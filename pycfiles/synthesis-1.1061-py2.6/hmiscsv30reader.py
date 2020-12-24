# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/hmiscsv30reader.py
# Compiled at: 2010-11-24 16:12:55
"""Reads a a set of HMIS CSV files into memory, parses their contents, and stores 
their informaton into a postgresql database.  This is a log database, so it holds 
everything and doesn't worry about deduplication.  The only thing it enforces 
are exportids, which must be unique."""
import sys, os
from reader import Reader
from zope.interface import implements
from lxml import etree
from sqlalchemy.exceptions import IntegrityError
import dateutil.parser
from conf import settings
import clsExceptions, DBObjects
from fileUtils import fileUtilities
from errcatalog import catalog

class HmisCsv30Reader(DBObjects.databaseObjects):
    """Implements reader interface."""
    global FILEUTIL
    implements(Reader)
    hmis_namespace = None
    airs_namespace = None
    nsmap = None
    FILEUTIL = fileUtilities(settings.DEBUG, None)

    def __init__(self, dir_name):
        pass


if __name__ == '__main__':
    sys.exit(main())
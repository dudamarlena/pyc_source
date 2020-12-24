# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/plugins/fileinfo_inv_plugin_ttf.py
# Compiled at: 2008-11-13 14:46:51
"""A fileinfo plug-in for TrueType fonts.

This needs the 'reportlab' package to be installed.

See also: 

  http://www.reportlab.org
"""
import re, sys, os.path, operator
try:
    from reportlab.pdfbase.ttfonts import TTFontParser
    HAVE_REPORTLAB = True
except ImportError:
    print "WARNING: Package 'reportlab' (needed for TTFInvestigator) not found."
    print 'Please install from reportlab.org if you want to use this plug-in!'
    HAVE_REPORTLAB = False

from fileinfo.investigator import BaseInvestigator

class Record:
    __module__ = __name__


class Null:
    """A class for implementing Null objects."""
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        """Ignore parameters."""
        return

    def __call__(self, *args, **kwargs):
        """Ignore method calls."""
        return self

    def __getattr__(self, mname):
        """Ignore attribute requests."""
        return self

    def __setattr__(self, name, value):
        """Ignore attribute setting."""
        return self

    def __delattr__(self, name):
        """Ignore deleting attributes."""
        return self

    def __repr__(self):
        """Return a string representation."""
        return '<None>'

    def __str__(self):
        """Convert to a string and return it."""
        return 'None'

    def __nonzero__(self):
        """Convert to a string and return it."""
        return False


TRUETYPE_TABLE_DESC = {'head': ['version:ulong', 'version=version/2**16', 'unitsPerEm:ushort'], 'maxp': ['version:ulong', 'numGlyphs:ushort'], 'name': ['format:ushort', 'count:ushort'], 'kern': ['nPairs:ushort']}

def getTableRecord(ttfParser, tableName):
    """Return a table in a TTF file as a record."""
    try:
        ttfParser.seek_table(tableName)
    except KeyError:
        return Null()

    rec = Record()
    for entry in TRUETYPE_TABLE_DESC[tableName]:
        if '=' in entry:
            (name, expr) = entry.split('=')
            val = eval(expr, globals(), rec.__dict__)
            setattr(rec, name, val)
        elif ':' in entry:
            (name, typ) = entry.split(':')
            if typ == 'longlong':
                tag1 = getattr(ttfParser, 'read_tag')()
                tag2 = getattr(ttfParser, 'read_tag')()
                val = tag1 + tag2
            else:
                val = getattr(ttfParser, 'read_' + typ)()
            setattr(rec, name, val)

    return rec


class TTFInvestigator(BaseInvestigator):
    """A class for determining attributes of TrueType files."""
    __module__ = __name__
    attrMap = {'head.unitsPerEm': None, 'maxp.version': None, 'maxp.numGlyphs': None, 'kern.nPairs': None}

    def activate(self):
        """Try activating self, setting 'active' variable."""
        if not HAVE_REPORTLAB:
            self.active = False
            return self.active
        try:
            self.p = TTFontParser(self.path)
            self.active = True
        except:
            self.active = False

        return self.active

    def getFunc(self, attrName):
        funcName = self.attrMap[attrName]
        if funcName != None:
            return getattr(self, funcName)
        else:
            return self.get
        return

    def getAttrValue(self, attrName):
        """Return value for attribute named 'attrName'."""
        if attrName in self.attrMap.keys():
            funcName = self.attrMap[attrName]
            if funcName == None:
                return self.getTtfAttr(attrName)
            return getattr(self, funcName)()
        else:
            matchingAttrNames = [ an for an in self.attrMap.keys() if re.match(an, attrName) ]
            if matchingAttrNames:
                funcName = self.attrMap[matchingAttrNames[0]]
                return getattr(self, funcName)(attrName)
        return

    def getTtfAttr(self, attr):
        """Return respective TrueType 'table.attribute'."""
        (tableName, attrName) = attr.split('.')
        if not hasattr(self, tableName):
            setattr(self, tableName, getTableRecord(self.p, tableName))
        return getattr(getattr(self, tableName), attrName)

    def get(self, attr):
        """Return respective TrueType 'table.attribute'."""
        (tableName, attrName) = attr.split('.')
        if not hasattr(self, tableName):
            setattr(self, tableName, getTableRecord(self.p, tableName))
        return getattr(getattr(self, tableName), attrName)
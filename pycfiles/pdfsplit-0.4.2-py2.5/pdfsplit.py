# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/pdfsplit.py
# Compiled at: 2008-09-17 07:56:21
"""Split a PDF file or rearrange its pages into a new PDF file.

This is a module for reading a PDF file, splitting it into single 
pages and reassembling selected single pages or page ranges into 
a new PDF document stored into a new file.

This module can be considered a sample tool for the excellent
package pyPdf by Mathieu Fenniak, see http://pybrary.net/pyPdf.

For further information please look into the file README.txt!
"""
import re, sys, getopt, os.path
try:
    import pyPdf
except ImportError:
    _MSG = 'Please install pyPdf first, see http://pybrary.net/pyPdf'
    raise RuntimeError(_MSG)

__version__ = '0.4.2'
__license__ = 'GPL 3'
__author__ = 'Dinu Gherman'
__date__ = '2008-09-17'
DEFAULT_BASENAME_POSTFIX_TAG = '-split'

def intOrNone(aString):
    """Convert a string to an integer, if possible, or None."""
    try:
        return int(aString)
    except ValueError:
        return

    return


def sliceStr2sliceObj(aString):
    """Convert a slice or index string like '::2' to a Python slice object.
    
    Slices are supposed to start at index 0, like in Python.
    
    E.g. 
    "0" -> slice(0, 1, None)
    "1:30" -> slice(1, 30, None)
    "1:30:2" -> slice(1, 30, 2)
    
    Raises a TypeError, if 'aString' doesn't contain 1-3 integers,
    seperated by ':'.
    """
    whitespace = '\t\n\x0b\x0c\r '
    for ch in whitespace:
        aString = aString.replace(ch, '')

    components = aString.split(':')
    length = len(components)
    if length == 0 or length >= 4:
        raise TypeError
    elif length == 1:
        i = intOrNone(components[0])
        assert type(i) == int
        if i >= 0:
            res = (
             i, i + 1, None)
        elif i == -1:
            res = (
             i, None, None)
        else:
            res = (
             i, i + 1, None)
    elif length == 2:
        res = (
         intOrNone(components[0]), intOrNone(components[1]), None)
    elif length == 3:
        res = tuple([ intOrNone(comp) for comp in components ])
    return slice(*res)


def rangeStr2sliceObj(aString):
    """Convert a range string like '18-35' to a Python slice object.
    
    In this case slices are supposed to start at index 1
    because page numbers usually are counted from 1, not 0.
    
    E.g. 
    "1" -> slice(0, 1, None)
    "1-3" -> slice(1, 4, None)

    Raises a ValueError, if 'aString' is not a valid range string.
    """
    try:
        val = int(aString)
        return slice(val - 1, val, None)
    except ValueError:
        pass

    pat = re.compile('(\\d+)\\-(\\d+)')
    m = re.match(pat, aString)
    if m:
        (start, end) = map(int, m.groups())
        if start > end:
            raise ValueError, "Not a valid range string: '%s'" % aString
        return slice(start - 1, end, None)
    raise ValueError, "Not a valid range string: '%s'" % aString
    return


def splitPages(path, slices, outputPat=None, indexPats=''):
    """Load selected pages from a PDF file and save them to another PDF file.

    'path' is the path of the input PDF file, 'slices' is a list 
    of Python slice objects, 'outputPat' is a string describing 
    the output filename with certain string formats expanded for
    each file (%(dirname)s, %(base)s, %(indices)s, and %(ext)s), 
    and 'indexPats' is an optional list of strings from which the 
    slices were generated (on the command-line).
    """
    if not outputPat:
        fmt = '%%(dirname)s/%%(base)s%s%%(ext)s'
        outputPat = fmt % DEFAULT_BASENAME_POSTFIX_TAG
    reader = pyPdf.PdfFileReader(file(path, 'rb'))
    writer = pyPdf.PdfFileWriter()
    inputPages = [ reader.getPage(i) for i in range(reader.getNumPages()) ]
    for aSlice in slices:
        if type(aSlice) == str:
            aSlice = sliceStr2sliceObj(aSlice)
        pages = inputPages[aSlice]
        for page in pages:
            writer.addPage(page)

    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    base = os.path.basename(os.path.splitext(path)[0])
    ext = os.path.splitext(path)[1]
    indices = (',').join(indexPats)
    aDict = {'dirname': dirname, 
       'basename': basename, 'base': base, 
       'indices': indices, 'ext': ext}
    outPath = outputPat % aDict
    outputStream = file(outPath, 'wb')
    writer.write(outputStream)
    print 'written: %s' % outPath
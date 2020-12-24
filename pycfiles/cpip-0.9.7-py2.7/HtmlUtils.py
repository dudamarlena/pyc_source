# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/HtmlUtils.py
# Compiled at: 2017-10-03 13:07:16
"""HTML utility functions."""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import os, hashlib, sys
from . import XmlWrite
from cpip.util import DictTree

def retHtmlFileName(thePath):
    """Creates a unique, short, human readable file name base on the input
    file path."""
    if sys.version_info[0] == 2:
        myBy = bytes(os.path.normpath(thePath))
    elif sys.version_info[0] == 3:
        myBy = bytes(os.path.normpath(thePath), 'ascii')
    else:
        assert 0, 'Unknown Python version %d' % sys.version_info.major
    myHash = hashlib.md5(myBy).hexdigest()
    return '%s_%s%s' % (os.path.basename(thePath), myHash, '.html')


def retHtmlFileLink(theSrcPath, theLineNum):
    """Returns a string that is a link to a HTML file.
    
    *theSrcPath : str*
        The path of the original source, whis will be encoded with retHtmlFileName().
    *theLineNum : int*
        An integer line number in the target.
    """
    return '%s#%d' % (retHtmlFileName(theSrcPath), theLineNum)


def writeHtmlFileLink(theS, theSrcPath, theLineNum, theText='', theClass=None):
    """Writes a link to another HTML file that represents source code.
    
    *theS*
        The XHTML stream.
    *theSrcPath : str*
        The path of the original source, this will be encoded with retHtmlFileName().
    *theLineNum : int*
        An integer line number in the target.
    *theText : str, optional*
        Navigation text.
    *theClass : obj, optional*
        CSS class for the navigation text.
    """
    with XmlWrite.Element(theS, 'a', {'href': retHtmlFileLink(theSrcPath, theLineNum)}):
        if theText:
            if theClass is None:
                theS.characters(theText)
            else:
                with XmlWrite.Element(theS, 'span', {'class': theClass}):
                    theS.characters(theText)
    return


def writeCharsAndSpan(theS, theText, theSpan):
    """Write theText to the stream theS. If theSpan is not None the text is
    enclosed in a ``<span class=theSpan>`` element.

    *theS*
        The XHTML stream.
    *theText : str*
        The text to write, must be non-empty.
    *theClass : str, optional*
        CSS class for the text.
    """
    assert theText
    if theSpan is None:
        theS.characters(theText)
    else:
        with XmlWrite.Element(theS, 'span', {'class': theSpan}):
            theS.characters(theText)
    return


def writeHtmlFileAnchor(theS, theLineNum, theText='', theClass=None, theHref=None):
    """Writes an anchor.
    
    *theS*
        The XHTML stream.
    *theLineNum : int*
        An integer line number in the target.
    *theText : str, optional*
        Navigation text.
    *theClass : str, optional*
        CSS class for the navigation text.
    *theHref : str, optional*
        The href=.
    """
    with XmlWrite.Element(theS, 'a', {'name': '%d' % theLineNum}):
        pass
    if theText:
        if theHref is None:
            writeCharsAndSpan(theS, theText, theClass)
        else:
            with XmlWrite.Element(theS, 'a', {'href': theHref}):
                writeCharsAndSpan(theS, theText, theClass)
    return


def pathSplit(p):
    """Split a path into its components."""
    p = os.path.normpath(p)
    l = p.split(os.sep)
    retVal = [ '%s%s' % (d, os.sep) for d in l[:-1] ]
    retVal.append(l[(-1)])
    return retVal


def writeFileListAsTable(theS, theFileLinkS, tableAttrs, includeKeyTail):
    """Writes a list of file names as an HTML table looking like a directory
    structure. theFileLinkS is a list of pairs (file_path, href).
    The navigation text in the cell will be the basename of the file_path."""
    myDict = DictTree.DictTreeHtmlTable(None)
    for f, h in theFileLinkS:
        keyList = pathSplit(f)
        myDict.add(keyList, (h, os.path.basename(f)))

    writeDictTreeAsTable(theS, myDict, tableAttrs, includeKeyTail)
    return


def writeFileListTrippleAsTable(theS, theFileLinkS, tableAttrs, includeKeyTail):
    """Writes a list of file names as an HTML table looking like a directory
    structure. *theFileLinkS* is a list of triples ``(file_name, href, nav_text)``."""
    myDict = DictTree.DictTreeHtmlTable('list')
    for f, h, n in theFileLinkS:
        keyList = pathSplit(f)
        myDict.add(keyList, (h, n))

    writeDictTreeAsTable(theS, myDict, tableAttrs, includeKeyTail)


def writeDictTreeAsTable(theS, theDt, tableAttrs, includeKeyTail):
    """Writes a DictTreeHtmlTable object as a table, for example as a directory
    structure.
    
    The key list in the DictTreeHtmlTable object is the path to the file
    i.e. ``os.path.abspath(p).split(os.sep)`` and the value is expected to be a
    pair of ``(link, nav_text)`` or ``None``."""
    myAttrs = {}
    try:
        myAttrs['class'] = tableAttrs['class']
    except KeyError:
        pass

    with XmlWrite.Element(theS, 'table', tableAttrs):
        for anEvent in theDt.genColRowEvents():
            if anEvent == theDt.ROW_OPEN:
                theS.startElement('tr', {})
            elif anEvent == theDt.ROW_CLOSE:
                theS.endElement('tr')
            else:
                k, v, r, c = anEvent
                myTdAttrs = {}
                myTdAttrs.update(myAttrs)
                if r > 1:
                    myTdAttrs['rowspan'] = '%d' % r
                if c > 1:
                    myTdAttrs['colspan'] = '%d' % c
                with XmlWrite.Element(theS, 'td', myTdAttrs):
                    if v is not None:
                        if includeKeyTail:
                            theS.characters('%s:' % k[(-1)])
                        if type(v) == list:
                            for h, n in v:
                                theS.characters(' ')
                                with XmlWrite.Element(theS, 'a', {'href': h}):
                                    theS.characters('%s' % n)

                        elif type(v) == tuple and len(v) == 2:
                            with XmlWrite.Element(theS, 'a', {'href': v[0]}):
                                theS.characters(v[1])
                        else:
                            theS.characters(str(v))
                    else:
                        theS.characters(k[(-1)])

    return


def writeFilePathsAsTable(valueType, theS, theKvS, tableStyle, fnTd, fnTrTh=None):
    """Writes file paths as a table, for example as a directory structure.
    
    *valueType*
        The type of the value: ``None, |'list' | 'set'``
    *theS*
        The HTML stream.
    *theKvS: list*
        A list of pairs ``(file_path, value)``.
    *tableStyle: str*
        The style used for the table.
    *fnTd*
        A callback function that is executed for a ``<td>`` element when
        there is a non-None value. This is called with the following arguments:
        
            *theS*
                The HTML stream.
                
            *attrs : dict*
                A map of attrs that include the rowspan/colspan for the <td>
                
            *k : list*
                The key as a list of path components.
                
            *v*
                The value given by the caller.
    *fnTrTh*
        Callback function for the header that will be called with the following
        arguments:
        
            *theS*
                The HTML stream.
                
            *pathDepth*
                Maximum depth of the largest path, this can be used for
                <th colspan="...">File path</th>.
    """
    myDict = DictTree.DictTreeHtmlTable(valueType)
    for k, v in theKvS:
        myDict.add(pathSplit(k), v)

    with XmlWrite.Element(theS, 'table', {'class': tableStyle}):
        if fnTrTh is not None:
            fnTrTh(theS, myDict.depth())
        for anEvent in myDict.genColRowEvents():
            if anEvent == myDict.ROW_OPEN:
                theS.startElement('tr', {})
            elif anEvent == myDict.ROW_CLOSE:
                theS.endElement('tr')
            else:
                k, v, r, c = anEvent
                myTdAttrs = {'class': tableStyle}
                if r > 1:
                    myTdAttrs['rowspan'] = '%d' % r
                if c > 1:
                    myTdAttrs['colspan'] = '%d' % c
                if v is not None:
                    fnTd(theS, myTdAttrs, k, v)
                else:
                    with XmlWrite.Element(theS, 'td', myTdAttrs):
                        theS.characters(k[(-1)])

    return
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/io/IOBase.py
# Compiled at: 2019-12-11 16:37:52
"""Base classes for sutekh.io card set parsers and writers.
   """
import logging
from xml.etree.ElementTree import parse, tostring
try:
    from xml.etree.ElementTree import ParseError
except ImportError:
    from xml.parsers.expat import ExpatError as ParseError

from sqlobject import sqlhub
from ..Utility import pretty_xml, norm_xml_quotes
from ..core.DBUtility import flush_cache

class CardSetParser(object):
    """Parent class for card set parsers.

       Card set parser classes need not subclass this class, only
       create a card set parser object when called without arguments.
       The parser object should have a .parse() method that takes a
       file-like object and a card set holder as parameters.

       Example:
           oParser = cParser()
           oParser.parse(fIn, oCardSetHolder)
       """

    def parse(self, fIn, oHolder):
        """Parse the card set in the file-like object fIn into the card
           set holder oHolder.
           """
        raise NotImplementedError('CardSetParser should be sub-classed')


class CardSetWriter(object):
    """Parent class for card set writers.

       Card set writer classes need not subclass this class, only
       create a card set writer object when called without arguments.
       The writer object should have a .write() method that takes a
       file-like object and a card set holder as parameters.

       Example:
           oWriter = cWriter()
           oWriter.write(fOut, oHolder)

       The sutekh.base.core.CardSetHolder module provides a CardSetWrapper
       implementation of the CardSetHolder class for use when writing
       out an existing card set.

       Example:
           from sutekh.base.core.CardSetHolder import CardSetWrapper
           oWriter.write(fOut, CardSetWrapper(oCS))
       """

    def write(self, fOut, oHolder):
        """Write the card set in the card set holder to the file-like
           object fOut.
           """
        raise NotImplementedError('CardSetWriter should be sub-classed')


class BaseXMLParser(object):
    """Base object for the various XML Parser classes.

       classes just implement a _convert_tree class to fill in the
       card set holder from the XML tree."""

    def __init__(self):
        self._oTree = None
        return

    def _convert_tree(self, oHolder):
        """Convert the XML Tree into a card set holder"""
        raise NotImplementedError('BaseXMLParser should be subclassed')

    def parse(self, fIn, oHolder):
        """Read the XML tree from the file-like object fIn"""
        try:
            self._oTree = parse(fIn)
        except ParseError as oExp:
            raise IOError('Not an XML file: %s' % oExp)

        self._convert_tree(oHolder)


class BaseLineParser(CardSetParser):
    """Base class for simple line-by-line parsers.

       Subclasses override _feed to handle the individual lines
       """

    def _feed(self, sLine, oHolder):
        """Internal method to handle a single line. Overriden by the
           subclasses"""
        raise NotImplementedError('BaseLineParser should be subclassed')

    def parse(self, fIn, oHolder):
        """Parse the file line by line"""
        for sLine in fIn:
            sLine = sLine.strip()
            if not sLine:
                continue
            self._feed(sLine, oHolder)


class BaseXMLWriter(CardSetWriter):
    """Base class for XML output"""

    def _gen_tree(self, oHolder):
        """Create the XML Tree"""
        raise NotImplementedError('BaseXMLWriter should be subclassed')

    def write(self, fOut, oHolder):
        """Write the holder contents as pretty XML to the given file-like
           object fOut"""
        oRoot = self._gen_tree(oHolder)
        pretty_xml(oRoot)
        sData = tostring(oRoot)
        sData = norm_xml_quotes(sData)
        fOut.write(sData)


class SlienceFilter(logging.Filter):
    """Silence all logging during the cache updates"""

    def filter(self, _record):
        """We allow nothing through"""
        return 0


def safe_parser(oFile, oParser):
    """Wrap the logic for parsing files, to ensure we
       handle transactions and error conditions consistently.

       oFile is an object with a .open() method (e.g. EncodedFile).
       oParser is an object with a parse() method that takes an
       open file object."""
    oRootLogger = logging.getLogger()
    oFilter = SlienceFilter()
    oRootLogger.addFilter(oFilter)
    flush_cache()
    oRootLogger.removeFilter(oFilter)
    fIn = None
    oOldConn = sqlhub.processConnection
    sqlhub.processConnection = oOldConn.transaction()
    try:
        fIn = oFile.open()
        oParser.parse(fIn)
        sqlhub.processConnection.commit(close=True)
    finally:
        if fIn:
            fIn.close()
        sqlhub.processConnection = oOldConn

    return
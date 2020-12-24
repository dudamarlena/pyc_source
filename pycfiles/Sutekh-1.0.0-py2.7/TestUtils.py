# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/tests/TestUtils.py
# Compiled at: 2019-12-11 16:37:52
"""Utilities and support classes that are useful for testing."""
import unittest, tempfile, os, sys, StringIO
from logging import FileHandler
import gtk
from nose import SkipTest
from ..core.BaseAdapters import IAbstractCard, IPhysicalCard, IExpansion, IPrinting

def make_card(sCardName, sExpName, sPrinting=None):
    """Create a Physical card given the name and expansion.

       Handle None for the expansion name properly"""
    if sExpName:
        oExp = IExpansion(sExpName)
        oPrinting = IPrinting((oExp, sPrinting))
    else:
        oPrinting = None
    oAbs = IAbstractCard(sCardName)
    oCard = IPhysicalCard((oAbs, oPrinting))
    return oCard


def create_tmp_file(sDir, sData):
    """Create a temporary file in the given directory."""
    fTemp, sFilename = tempfile.mkstemp(dir=sDir)
    os.close(fTemp)
    if sData:
        fTmp = open(sFilename, 'wb')
        fTmp.write(sData)
        fTmp.close()
    return sFilename


def create_pkg_tmp_file(sData):
    """Create a temporary file for use in package setup."""
    return create_tmp_file(None, sData)


class BaseTestCase(unittest.TestCase):
    """Base class for tests.

       Define some useful helper methods.
       """
    TEST_CONN = None
    PREFIX = 'testcase'

    @classmethod
    def set_db_conn(cls, oConn):
        """Set the class connection to the correct global conn for later use"""
        cls.TEST_CONN = oConn

    def _create_tmp_file(self, sData=None):
        """Creates a temporary file with the given data, closes it and returns
           the filename."""
        sFilename = create_tmp_file(self._sTempDir, sData)
        self._aTempFiles.append(sFilename)
        return sFilename

    def _setUpTemps(self):
        """Create a directory to hold the temporary files."""
        self._sTempDir = tempfile.mkdtemp(suffix='dir', prefix=self.PREFIX)
        self._aTempFiles = []

    def _tearDownTemps(self):
        """Clean up the temporary files."""
        for sFile in self._aTempFiles:
            if os.path.exists(sFile):
                os.remove(sFile)

        os.rmdir(self._sTempDir)
        self._sTempDir = None
        self._aTempFiles = None
        return

    def _round_trip_obj(self, oWriter, oObj):
        """Round trip an object through a temporary file.

           Common operation for the writer tests."""
        sTempFile = self._create_tmp_file()
        fOut = open(sTempFile, 'w')
        oWriter.write(fOut, oObj)
        fOut.close()
        fIn = open(sTempFile, 'rU')
        sData = fIn.read()
        fIn.close()
        return sData

    def _make_holder_from_string(self, oParser, sString):
        """Read the given string into a DummyHolder.

           common operation for the parser tests"""
        oHolder = DummyHolder()
        oParser.parse(StringIO.StringIO(sString), oHolder)
        return oHolder


class DummyHolder(object):
    """Emulate CardSetHolder for test purposes."""

    def __init__(self):
        self.dCards = {}
        self.name = ''
        self.comment = ''
        self.author = ''
        self.annotations = ''

    def add(self, iCnt, sName, sExpName, sPrintingName):
        """Add a card to the dummy holder."""
        self.dCards.setdefault((sName, sExpName, sPrintingName), 0)
        self.dCards[(sName, sExpName, sPrintingName)] += iCnt

    def get_cards_exps(self):
        """Get the cards with expansions"""
        return self.dCards.items()

    def get_cards(self):
        """Get the card info without expansions"""
        dNoExpCards = {}
        for tKey in self.dCards:
            sCardName = tKey[0]
            dNoExpCards.setdefault(sCardName, 0)
            dNoExpCards[sCardName] += self.dCards[tKey]

        return dNoExpCards.items()


class GuiBaseTest(unittest.TestCase):
    """Adds useful methods for gui test cases."""

    def setUp(self):
        """Check if we should run the gui tests."""
        if gtk.gdk.screen_get_default() is None:
            raise SkipTest
        os.environ['UBUNTU_MENUPROXY'] = '0'
        super(GuiBaseTest, self).setUp()
        return

    def tearDown(self):
        """Cleanup gtk state after test."""
        while gtk.events_pending():
            gtk.main_iteration()

        super(GuiBaseTest, self).tearDown()


def make_null_handler():
    """Utility function to create a logger for /dev/null that works
       on both windows and Linux"""
    if sys.platform.startswith('win'):
        return FileHandler('NUL')
    return FileHandler('/dev/null')


class FailFile(object):
    """File'ish that raises exceptions for checking error handler stuff"""

    def __init__(self, oExp):
        self._oExp = oExp

    def read(self):
        """Dummy method"""
        raise self._oExp
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/Utility.py
# Compiled at: 2019-12-11 16:37:52
"""Misc generic functions needed in various places."""
import datetime, logging, os, re, sys, tempfile, urlparse
from sqlobject import sqlhub

def gen_temp_file(sBaseName, sDir):
    """Simple wrapper around tempfile creation - generates the name and closes
       the file
       """
    fTemp, sFilename = tempfile.mkstemp('.xml', sBaseName, sDir)
    os.close(fTemp)
    return sFilename


def gen_app_temp_dir(sApp):
    """Create a temporary directory using mkdtemp"""
    sTempdir = tempfile.mkdtemp('dir', sApp)
    return sTempdir


def safe_filename(sFilename):
    """Replace potentially dangerous and annoying characters in the name -
       used to automatically generate sensible filenames from card set names
       """
    sSafeName = sFilename
    sSafeName = sSafeName.replace(' ', '_')
    sSafeName = sSafeName.replace('/', '_')
    sSafeName = sSafeName.replace('\\', '_')
    return sSafeName


def prefs_dir(sApp):
    """Return a suitable directory for storing preferences and other
       application data."""
    if sys.platform.startswith('win') and 'APPDATA' in os.environ:
        return os.path.join(os.environ['APPDATA'], sApp)
    return os.path.join(os.path.expanduser('~'), '.%s' % sApp.lower())


def ensure_dir_exists(sDir):
    """Check that a directory exists and create it if it doesn't.
       """
    if os.path.exists(sDir):
        assert os.path.isdir(sDir)
    else:
        os.makedirs(sDir)


def sqlite_uri(sPath):
    """Create an SQLite db URI from the path to the db file.
       """
    sDbFile = sPath.replace(os.sep, '/')
    sDrive, sRest = os.path.splitdrive(sDbFile)
    if sDrive:
        sDbFile = '/' + sDrive.rstrip(':') + '|' + sRest
    else:
        sDbFile = sRest
    return 'sqlite://' + sDbFile


def pretty_xml(oElement, iIndentLevel=0):
    """
    Helper function to add whitespace text attributes to a ElementTree.
    Makes for 'pretty' indented XML output.
    Based on the example indent function at
    http://effbot.org/zone/element-lib.htm [22/01/2008]
    """
    sIndent = '\n' + iIndentLevel * '  '
    if len(oElement):
        if not oElement.text or not oElement.text.strip():
            oElement.text = sIndent + '  '
            for oSubElement in oElement:
                pretty_xml(oSubElement, iIndentLevel + 1)

            if not oSubElement.tail or not oSubElement.tail.strip():
                oSubElement.tail = sIndent
    elif iIndentLevel and (not oElement.tail or not oElement.tail.strip()):
        oElement.tail = sIndent


def norm_xml_quotes(sData):
    """Normalise quote escaping from ElementTree, to hide version
       differences"""
    return sData.replace('&apos;', "'")


def get_database_url():
    """Return the database url, with the password stripped out if
       needed"""
    sDBuri = sqlhub.processConnection.uri()
    tParsed = urlparse.urlsplit(sDBuri)
    if tParsed.password:
        tCombined = (
         tParsed.scheme,
         tParsed.netloc.replace(tParsed.password, '****'),
         tParsed.path, tParsed.query, tParsed.fragment)
        sUrl = urlparse.urlunsplit(tCombined)
    else:
        sUrl = sDBuri
    return sUrl


def move_articles_to_back(sName):
    """Moves articles to the end of the name.

       Reverse of move_articles_to_front.
       Used when exporting to various formats and when selected
       as a display option."""
    if sName.startswith('The '):
        sName = sName[4:] + ', The'
    elif sName.startswith('An '):
        sName = sName[3:] + ', An'
    elif sName.startswith('A '):
        sName = sName[2:] + ', A'
    return sName


def move_articles_to_front(sName):
    """Moves articles from the end back to the start as is expected
       in the database.

       Reverses move_articles_to_back.
       Used when importing from various formats."""
    if sName.lower().endswith(', the'):
        sName = 'The ' + sName[:-5]
    elif sName.lower().endswith(', an'):
        sName = 'An ' + sName[:-4]
    elif sName.lower().endswith(', a'):
        sName = 'A ' + sName[:-3]
    return sName


def normalise_whitespace(sText):
    """Return a copy of sText with all whitespace normalised to single
       spaces."""
    return re.sub('\\s+', ' ', sText, flags=re.MULTILINE).strip()


def find_subclasses(cClass):
    """Utility method to find the subclasses of a specific class.

       Used for introspection magic to lookup various stuff without importing
       it directly from the main application.

       Because we expect liberal use of overloading, this only returns
       classes which have no subclasses themselves, so overloading a base
       Filter to tweak behaviour will only return the overloaded filter,
       rather than both.

       To avoid issues with diamond inheritance, we return an unordered set
       of the subclasses."""
    aSubClasses = set()
    for oChild in cClass.__subclasses__():
        aSubClasses.update(find_subclasses(oChild))

    if not cClass.__subclasses__():
        aSubClasses.add(cClass)
    return aSubClasses


def setup_logging(bVerbose, sErrFile=None):
    """Setup the log handling for this run"""
    oRootLogger = logging.getLogger()
    oRootLogger.setLevel(level=logging.DEBUG)
    if bVerbose or sErrFile:
        bSkipVerbose = False
        if sErrFile:
            try:
                oLogHandler = logging.FileHandler(sErrFile)
                oRootLogger.addHandler(oLogHandler)
            except IOError:
                oLogHandler = logging.StreamHandler(sys.stderr)
                oRootLogger.addHandler(oLogHandler)
                bSkipVerbose = True
                logging.error('Unable to open log file, logging to stderr', exc_info=1)

        if bVerbose and not bSkipVerbose:
            oLogHandler = logging.StreamHandler(sys.stderr)
            oRootLogger.addHandler(oLogHandler)
    else:
        oLogHandler = logging.StreamHandler(sys.stderr)
        oRootLogger.addHandler(oLogHandler)
        oLogHandler.setLevel(level=logging.CRITICAL)
    return oRootLogger


def get_printing_date(oPrinting):
    """Return the release date for this printing as a date object."""
    for oProp in oPrinting.properties:
        if oProp.value.startswith('Release Date:'):
            sDate = oProp.value.split(':', 1)[1].strip()
            oDate = datetime.datetime.strptime(sDate, '%Y-%m-%d').date()
            return oDate

    return


def get_expansion_date(oExp):
    """Get the date of the default printing as a date object."""
    for oPrint in oExp.printings:
        if oPrint.name is None:
            return get_printing_date(oPrint)

    return


def is_memory_db():
    """Helper function to test if we are using a memory db.

       returns True if this is a memory db"""
    return sqlhub.processConnection.uri() in ('sqlite:///:memory:', 'sqlite:/:memory:')
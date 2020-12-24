# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/bioio.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 12289 bytes
from __future__ import absolute_import
from builtins import range
from builtins import object
import socket, sys, os, logging, resource, logging.handlers, tempfile, random, math, shutil
from argparse import ArgumentParser
from optparse import OptionContainer, OptionGroup
import subprocess
from six.moves import xrange
from six import string_types
import xml.etree.cElementTree as ET
from xml.dom import minidom
defaultLogLevel = logging.INFO
logger = logging.getLogger(__name__)
rootLogger = logging.getLogger()
toilLogger = logging.getLogger('toil')

def getLogLevelString(logger=None):
    if logger is None:
        logger = rootLogger
    return logging.getLevelName(logger.getEffectiveLevel())


__loggingFiles = []

def addLoggingFileHandler(fileName, rotatingLogging=False):
    if fileName in __loggingFiles:
        return
    else:
        __loggingFiles.append(fileName)
        if rotatingLogging:
            handler = logging.handlers.RotatingFileHandler(fileName, maxBytes=1000000, backupCount=1)
        else:
            handler = logging.FileHandler(fileName)
        rootLogger.addHandler(handler)
        return handler


def setLogLevel(level, logger=None):
    """
    Sets the log level to a given string level (like "INFO"). Operates on the
    root logger by default, but another logger can be specified instead.
    """
    if logger is None:
        logger = rootLogger
    else:
        level = level.upper()
        if level == 'OFF':
            level = 'CRITICAL'
        numericLevel = logging.getLevelName(level)
        assert logging.getLevelName(numericLevel) == level
    logger.setLevel(numericLevel)
    logging.getLogger('boto').setLevel(logging.CRITICAL)


def logFile(fileName, printFunction=logger.info):
    """Writes out a formatted version of the given log file
    """
    printFunction('Reporting file: %s' % fileName)
    shortName = fileName.split('/')[(-1)]
    fileHandle = open(fileName, 'r')
    line = fileHandle.readline()
    while line != '':
        if line[(-1)] == '\n':
            line = line[:-1]
        printFunction('%s:\t%s' % (shortName, line))
        line = fileHandle.readline()

    fileHandle.close()


def logStream(fileHandle, shortName, printFunction=logger.info):
    """Writes out a formatted version of the given log stream.
    """
    printFunction('Reporting file: %s' % shortName)
    line = fileHandle.readline()
    while line != '':
        if line[(-1)] == '\n':
            line = line[:-1]
        printFunction('%s:\t%s' % (shortName, line))
        line = fileHandle.readline()

    fileHandle.close()


def addLoggingOptions(parser):
    if isinstance(parser, ArgumentParser):
        group = parser.add_argument_group('Logging Options', 'Options that control logging')
        _addLoggingOptions(group.add_argument)
    else:
        raise RuntimeError('Unanticipated class passed to addLoggingOptions(), %s. Expecting argparse.ArgumentParser' % parser.__class__)


supportedLogLevels = (logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)

def _addLoggingOptions(addOptionFn):
    """
    Adds logging options
    """
    defaultLogLevelName = logging.getLevelName(defaultLogLevel)
    addOptionFn('--logOff', dest='logLevel', default=defaultLogLevelName,
      action='store_const',
      const='CRITICAL',
      help='Same as --logCritical')
    for level in supportedLogLevels:
        levelName = logging.getLevelName(level)
        levelNameCapitalized = levelName.capitalize()
        addOptionFn(('--log' + levelNameCapitalized), dest='logLevel', default=defaultLogLevelName,
          action='store_const',
          const=levelName,
          help=('Turn on logging at level %s and above. (default is %s)' % (levelName, defaultLogLevelName)))

    addOptionFn('--logLevel', dest='logLevel', default=defaultLogLevelName, help=('Log at given level (may be either OFF (or CRITICAL), ERROR, WARN (or WARNING), INFO or DEBUG). (default is %s)' % defaultLogLevelName))
    addOptionFn('--logFile', dest='logFile', help='File to log in')
    addOptionFn('--rotatingLogging', dest='logRotating', action='store_true', default=False, help='Turn on rotating logging, which prevents log files getting too big.')


def setLoggingFromOptions(options):
    """
    Sets the logging from a dictionary of name/value options.
    """
    formatStr = ' '.join([socket.gethostname(), '%(asctime)s', '%(threadName)s',
     '%(levelname)s', '%(name)s:', '%(message)s'])
    logging.basicConfig(format=formatStr)
    rootLogger.setLevel(defaultLogLevel)
    if options.logLevel is not None:
        setLogLevel(options.logLevel)
    else:
        setLogLevel(getLogLevelString())
    logger.debug("Root logger is at level '%s', 'toil' logger at level '%s'.", getLogLevelString(logger=rootLogger), getLogLevelString(logger=toilLogger))
    if options.logFile is not None:
        addLoggingFileHandler((options.logFile), rotatingLogging=(options.logRotating))
        logger.debug("Logging to file '%s'." % options.logFile)


def system(command):
    """
    A convenience wrapper around subprocess.check_call that logs the command before passing it
    on. The command can be either a string or a sequence of strings. If it is a string shell=True
    will be passed to subprocess.check_call.

    :type command: str | sequence[string]
    """
    logger.debug('Running: %r', command)
    subprocess.check_call(command, shell=(isinstance(command, string_types)), bufsize=(-1))


def getTotalCpuTimeAndMemoryUsage():
    """
    Gives the total cpu time of itself and all its children, and the maximum RSS memory usage of
    itself and its single largest child.
    """
    me = resource.getrusage(resource.RUSAGE_SELF)
    childs = resource.getrusage(resource.RUSAGE_CHILDREN)
    totalCPUTime = me.ru_utime + me.ru_stime + childs.ru_utime + childs.ru_stime
    totalMemoryUsage = me.ru_maxrss + childs.ru_maxrss
    return (totalCPUTime, totalMemoryUsage)


def getTotalCpuTime():
    """Gives the total cpu time, including the children.
    """
    return getTotalCpuTimeAndMemoryUsage()[0]


def getTotalMemoryUsage():
    """Gets the amount of memory used by the process and its largest child.
    """
    return getTotalCpuTimeAndMemoryUsage()[1]


def absSymPath(path):
    """like os.path.abspath except it doesn't dereference symlinks
    """
    curr_path = os.getcwd()
    return os.path.normpath(os.path.join(curr_path, path))


class TestStatus(object):
    TEST_SHORT = 0
    TEST_MEDIUM = 1
    TEST_LONG = 2
    TEST_VERY_LONG = 3
    TEST_STATUS = TEST_SHORT
    SAVE_ERROR_LOCATION = None

    def getTestStatus():
        return TestStatus.TEST_STATUS

    getTestStatus = staticmethod(getTestStatus)

    def setTestStatus(status):
        assert status in (TestStatus.TEST_SHORT, TestStatus.TEST_MEDIUM, TestStatus.TEST_LONG, TestStatus.TEST_VERY_LONG)
        TestStatus.TEST_STATUS = status

    setTestStatus = staticmethod(setTestStatus)

    def getSaveErrorLocation():
        """Location to in which to write inputs which created test error.
        """
        return TestStatus.SAVE_ERROR_LOCATION

    getSaveErrorLocation = staticmethod(getSaveErrorLocation)

    def setSaveErrorLocation(dir):
        """Set location in which to write inputs which created test error.
        """
        logger.debug('Location to save error files in: %s' % dir)
        assert os.path.isdir(dir)
        TestStatus.SAVE_ERROR_LOCATION = dir

    setSaveErrorLocation = staticmethod(setSaveErrorLocation)

    def getTestSetup(shortTestNo=1, mediumTestNo=5, longTestNo=100, veryLongTestNo=0):
        if TestStatus.TEST_STATUS == TestStatus.TEST_SHORT:
            return shortTestNo
        else:
            if TestStatus.TEST_STATUS == TestStatus.TEST_MEDIUM:
                return mediumTestNo
            if TestStatus.TEST_STATUS == TestStatus.TEST_LONG:
                return longTestNo
            return veryLongTestNo

    getTestSetup = staticmethod(getTestSetup)

    def getPathToDataSets():
        """This method is used to store the location of
        the path where all the data sets used by tests for analysis are kept.
        These are not kept in the distrbution itself for reasons of size.
        """
        assert 'SON_TRACE_DATASETS' in os.environ
        return os.environ['SON_TRACE_DATASETS']

    getPathToDataSets = staticmethod(getPathToDataSets)


def getBasicOptionParser(parser=None):
    if parser is None:
        parser = ArgumentParser()
    addLoggingOptions(parser)
    parser.add_argument('--tempDirRoot', dest='tempDirRoot', type=str, help='Path to where temporary directory containing all temp files are created, by default uses the current working directory as the base.',
      default=(tempfile.gettempdir()))
    return parser


def parseBasicOptions(parser):
    """Setups the standard things from things added by getBasicOptionParser.
    """
    options = parser.parse_args()
    setLoggingFromOptions(options)
    if options.tempDirRoot == 'None':
        options.tempDirRoot = tempfile.gettempdir()
    return options


def getRandomAlphaNumericString(length=10):
    """Returns a random alpha numeric string of the given length.
    """
    return ''.join([random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(0, length)])


def makePublicDir(dirName):
    """Makes a given subdirectory if it doesn't already exist, making sure it is public.
    """
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        os.chmod(dirName, 511)
    return dirName


def getTempFile(suffix='', rootDir=None):
    """Returns a string representing a temporary file, that must be manually deleted
    """
    if rootDir is None:
        handle, tmpFile = tempfile.mkstemp(suffix)
        os.close(handle)
        return tmpFile
    else:
        tmpFile = os.path.join(rootDir, 'tmp_' + getRandomAlphaNumericString() + suffix)
        open(tmpFile, 'w').close()
        os.chmod(tmpFile, 511)
        return tmpFile
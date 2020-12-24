# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/conf/local_settings.py
# Compiled at: 2011-01-13 01:48:00
"""
locateSettings(dirname) returns the path were local settings will be stored

loadSettings(dirname, filename) returns the module object of the loaded prefs.py
found in the local settings directory

    Windows     based on APPDATA or USERPROFILE environment values plus
                "Application Data".  If that's not found, fall back
                to the HOMEDRIVE and HOMEPATH environment values.
    OS X        ~/Library/Appliction Support/windmill/
    Linux       ~/.windmill/
"""
import os, sys, platform, imp, glob, logging, traceback
logger = logging.getLogger(__name__)

def _dumpException():
    (t, v, tb) = sys.exc_info()
    return ('').join(traceback.format_exception(t, v, tb))


def locateSettings(dirName='windmill'):
    """
    Locate the platform specific directory where user configuration settings
    should be stored and return it.
    
    If the directory does not exist, then create it before returning.
    
    Unless overridden, the default name of 'windmill' will be used.
    """
    settingsDir = None
    dataDir = None
    if sys.platform == 'win32':
        if os.environ.has_key('APPDATA'):
            dataDir = os.environ['APPDATA']
        elif os.environ.has_key('USERPROFILE'):
            dataDir = os.environ['USERPROFILE']
            if os.path.isdir(os.path.join(dataDir, 'Application Data')):
                dataDir = os.path.join(dataDir, 'Application Data')
        if dataDir is None or not os.path.isdir(dataDir):
            if os.environ.has_key('HOMEDRIVE') and os.environ.has_key('HOMEPATH'):
                dataDir = '%s%s' % (os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])
        if dataDir is None or not os.path.isdir(dataDir):
            dataDir = os.path.expanduser('~')
        settingsDir = os.path.join(dataDir, dirName)
    elif sys.platform == 'darwin':
        dataDir = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support')
        settingsDir = os.path.join(dataDir, dirName)
    else:
        dataDir = os.path.expanduser('~')
        settingsDir = os.path.join(dataDir, '.%s' % dirName)
    if settingsDir is not None and not os.path.isdir(settingsDir):
        try:
            os.makedirs(settingsDir, 448)
        except:
            logger.error('Unable to create setting directory [%s]' % settingsDir)
            settingsDir = None

    return settingsDir


PREFS_HEADER = '# local windmill preferences file\n# warning - this file will be overwritten by windmill\n#           so any edits should be done while windmill\n#           is not active.\n\n'

def loadSettings(dirname=None, filename='prefs.py'):
    """
    Load the local settings .py file located in dirname called filename.
    
    If the directory contains no files, then create an empty file.
    """
    settingsDir = dirname
    result = None
    if settingsDir is None:
        settingsDir = locateSettings()
    if settingsDir is not None:
        prefsFile = os.path.join(settingsDir, filename)
        if not os.path.isfile(prefsFile):
            h = open(prefsFile, 'w')
            h.write(PREFS_HEADER)
            h.close()
        try:
            minfo = None
            result = None
            try:
                mname = os.path.splitext(filename)[0]
                minfo = imp.find_module(mname, [settingsDir])
                result = imp.load_module(mname, *minfo)
            except:
                logger.error('Error loading settings file [%s]' % prefsFile)
                logger.error(_dumpException())
                minfo = None
                result = None

        finally:
            if minfo is not None:
                minfo[0].close()

    return result


if __name__ == '__main__':
    if '--test' in sys.argv:
        testfile = 'bear.py'
        settingsDir = locateSettings()
        if settingsDir is None:
            print 'locateSettings() return a value of None'
            sys.exit(1)
        settingsFile = os.path.join(settingsDir, testfile)
        if os.path.isfile(settingsFile):
            print 'test file [%s] already present in [%s]' % (testfile, settingsDir)
        else:
            h = open(settingsFile, 'w')
            h.write('foo="bar"\nbar=2\n')
            h.close()
        settings = loadSettings(settingsDir, testfile)
        print 'foo = bar:', getattr(settings, 'foo', None)
        print 'bar = 2:  ', getattr(settings, 'bar', None)
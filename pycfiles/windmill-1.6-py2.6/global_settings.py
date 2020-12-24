# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_mozrunner/global_settings.py
# Compiled at: 2011-01-13 01:48:00
import os, sys, copy

def findInPath(fileName, path=None):
    if path is None:
        path = os.environ.get('PATH', '')
    dirs = path.split(os.pathsep)
    for dir in dirs:
        if os.path.isfile(os.path.join(dir, fileName)):
            return os.path.join(dir, fileName)
        elif os.name == 'nt' or sys.platform == 'cygwin':
            if os.path.isfile(os.path.join(dir, fileName + '.exe')):
                return os.path.join(dir, fileName + '.exe')

    return


MOZILLA_DEFAULT_PREFS = {'extensions.update.enabled': False, 'extensions.update.notifyUser': False, 
   'browser.shell.checkDefaultBrowser': False, 
   'browser.tabs.warnOnClose': False, 
   'browser.warnOnQuit': False, 
   'browser.sessionstore.resume_from_crash': False}
MOZILLA_PREFERENCES = {}
MOZILLA_CMD_ARGS = []
MOZILLA_ENV = copy.copy(os.environ)
MOZILLA_ENV.update({'MOZ_NO_REMOTE': '1'})
MOZILLA_CREATE_NEW_PROFILE = True
if sys.platform == 'darwin':
    NETWORK_INTERFACE_NAME = None
    firefoxApp = os.path.join('Applications', 'Firefox.app')
    firefoxDir = os.path.join(os.path.expanduser('~/'), firefoxApp)
    if not os.path.isdir(firefoxDir):
        firefoxDir = os.path.join('/', firefoxApp)
    MOZILLA_DEFAULT_PROFILE = os.path.join(firefoxDir, 'Contents', 'MacOS', 'defaults', 'profile')
    MOZILLA_BINARY = os.path.join(firefoxDir, 'Contents', 'MacOS', 'firefox-bin')
elif sys.platform == 'linux2':
    firefoxBin = findInPath('firefox')
    if firefoxBin is not None and os.path.isfile(firefoxBin):
        MOZILLA_BINARY = firefoxBin
    MOZILLA_DEFAULT_PROFILE = None

    def NaN(str):
        try:
            int(str)
            return False
        except:
            return True


    for (path, name) in (('/opt', 'firefox'),
     ('/usr/lib', 'iceweasel'),
     ('/usr/share', 'firefox'),
     ('/usr/lib', 'mozilla-firefox'),
     ('/usr/lib', 'firefox'),
     ('/usr/lib64', 'iceweasel'),
     ('/usr/lib64', 'mozilla-firefox'),
     ('/usr/lib64', 'firefox')):
        if os.path.isdir(path):
            profiles = sorted([ d for d in os.listdir(os.path.join(path)) if d.startswith(name) if os.path.isdir(os.path.join(path, d, 'defaults', 'profile')) if '-' not in d or len(name + '-') <= len(d) and not NaN(d[len(name + '-')]) or d == 'mozilla-firefox'
                              ])
            if len(profiles) > 0:
                MOZILLA_DEFAULT_PROFILE = os.path.join(path, profiles[(-1)], 'defaults', 'profile')

elif os.name == 'nt' or sys.platform == 'cygwin':
    firefoxBin = findInPath('firefox')
    if sys.platform == 'cygwin':
        program_files = os.environ['PROGRAMFILES'].replace('\\', os.path.sep).replace(':', '')
        program_files = program_files[0].lower() + program_files[1:]
        program_files = '/cygdrive/' + program_files.replace('\\', os.path.sep)
    else:
        program_files = os.environ['ProgramFiles']
    bin_locations = [os.path.join(program_files, 'Mozilla Firefox', 'firefox.exe'),
     os.path.join(program_files, 'Mozilla Firefox3', 'firefox.exe')]
    if firefoxBin is None:
        for loc in bin_locations:
            if os.path.isfile(loc):
                firefoxBin = loc

    if firefoxBin is not None and os.path.isfile(firefoxBin):
        firefoxDir = os.path.dirname(firefoxBin)
        MOZILLA_BINARY = firefoxBin
        MOZILLA_DEFAULT_PROFILE = os.path.join(firefoxDir, 'defaults', 'profile')
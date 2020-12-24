# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/apputils.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 4103 bytes
from noval import GetApp
import sys, os, time, pyperclip, psutil, locale, future.utils
MAINMODULE_DIR = 'NOVAL_MAINMODULE_DIR'

def is_windows():
    return os.name == 'nt'


def is_linux():
    return os.name == 'posix'


def is_py2():
    return future.utils.PY2


def is_py3():
    return future.utils.PY3


def is_py3_plus():
    return sys.version_info[0] >= 3


def get_default_encoding():
    try:
        return locale.getpreferredencoding()
    except:
        return locale.getdefaultlocale()[1]


def get_default_locale():
    return locale.getdefaultlocale()[0]


def _generateMainModuleDir():
    mainModuleDir = os.getenv(MAINMODULE_DIR)
    if mainModuleDir:
        if is_windows() and is_py2():
            return mainModuleDir.decode(get_default_encoding())
        return mainModuleDir
    sysExecLower = sys.executable.lower()
    if sysExecLower == '/' or sysExecLower.find('python') != -1:
        utilModuleDir = os.path.dirname(__file__)
        if not os.path.isabs(utilModuleDir):
            utilModuleDir = os.path.join(os.getcwd(), utilModuleDir)
        mainModuleDir = os.path.normpath(os.path.join(utilModuleDir, os.path.join(os.path.pardir, os.path.pardir)))
        if mainModuleDir.endswith('.zip'):
            mainModuleDir = os.path.dirname(mainModuleDir)
    else:
        mainModuleDir = os.path.dirname(sys.executable)
    os.environ[MAINMODULE_DIR] = mainModuleDir
    if is_windows() and is_py2():
        return mainModuleDir.decode(get_default_encoding())
    return mainModuleDir


mainModuleDir = _generateMainModuleDir()

def getCommandNameForExecPath(execPath):
    if isWindows():
        return '"%s"' % execPath
    return execPath


def getUserName():
    if isWindows():
        return os.getenv('USERNAME')
    else:
        return os.getenv('USER')


def getCurrentTimeAsFloat():
    return time.time()


systemStartTime = getCurrentTimeAsFloat()

def CopyToClipboard(str):
    if is_windows():
        pyperclip.copy(str)
    else:
        GetApp().clipboard_clear()
        GetApp().clipboard_append(str)


def GetSupportableExtList():
    exts = []
    for template in GetApp().GetDocumentManager().GetTemplates():
        filter = template.GetFileFilter()
        parts = filter.split(';')
        for part in parts:
            ext = part.replace('*.', '').strip()
            exts.append(ext)

    return exts


def is_ext_supportable(ext):
    if ext == '':
        return True
    return ext.lower() in GetSupportableExtList()


def get_app_version():
    versionFilepath = os.path.join(mainModuleDir, 'version.txt')
    if os.path.exists(versionFilepath):
        versionfile = open(versionFilepath, 'r')
        versionLines = versionfile.readlines()
        versionfile.close()
        version = ''.join(versionLines)
    else:
        version = 'Version Unknown - %s not found' % versionFilepath
    return version


def get_lang_config():
    config_path = os.path.join(mainModuleDir, 'config.ini')
    if not os.path.exists(config_path):
        return -1
    if is_py2():
        from ConfigParser import ConfigParser
    elif is_py3_plus():
        from configparser import ConfigParser
    cfg = ConfigParser()
    cfg.read(config_path)
    return int(cfg.get('IDE', 'Language'))
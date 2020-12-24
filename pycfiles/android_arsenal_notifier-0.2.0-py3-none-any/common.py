# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/com/dtmilano/android/common.py
# Compiled at: 2019-10-11 02:14:01
__doc__ = '\nCopyright (C) 2012-2018  Diego Torres Milano\nCreated on Jan 5, 2015\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n       http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n\n@author: Diego Torres Milano\n'
__version__ = '15.8.1'
import ast, os, platform, re

def _nd(name):
    """
    @return: Returns a named decimal regex
    """
    return '(?P<%s>\\d+)' % name


def _nh(name):
    """
    @return: Returns a named hex regex
    """
    return '(?P<%s>[0-9a-f]+)' % name


def _ns(name, greedy=False):
    """
    NOTICE: this is using a non-greedy (or minimal) regex

    @type name: str
    @param name: the name used to tag the expression
    @type greedy: bool
    @param greedy: Whether the regex is greedy or not

    @return: Returns a named string regex (only non-whitespace characters allowed)
    """
    return '(?P<%s>\\S+%s)' % (name, '' if greedy else '?')


def obtainPxPy(m):
    px = int(m.group('px'))
    py = int(m.group('py'))
    return (
     px, py)


def obtainVxVy(m):
    wvx = int(m.group('vx'))
    wvy = int(m.group('vy'))
    return (
     wvx, wvy)


def obtainVwVh(m):
    wvx, wvy = obtainVxVy(m)
    wvx1 = int(m.group('vx1'))
    wvy1 = int(m.group('vy1'))
    return (
     wvx1 - wvx, wvy1 - wvy)


def which(program, isWindows=False):
    import os

    def is_exe(_fpath, _isWindows):
        return os.path.isfile(_fpath) and os.access(_fpath, (_isWindows or os).X_OK if 1 else os.F_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program, isWindows):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file, isWindows):
                return exe_file

    return


def obtainAdbPath():
    """
    Obtains the ADB path attempting know locations for different OSs
    """
    FORCE_FAIL = False
    osName = platform.system()
    isWindows = False
    adb = 'adb'
    if osName.startswith('Windows') or osName.startswith('Java'):
        envOSName = os.getenv('os')
        if envOSName.startswith('Windows'):
            adb = 'adb.exe'
            isWindows = True
    exeFile = which(adb, isWindows)
    if exeFile:
        return exeFile
    else:
        ANDROID_HOME = os.environ['ANDROID_HOME'] if os.environ.has_key('ANDROID_HOME') else '/opt/android-sdk'
        HOME = os.environ['HOME'] if os.environ.has_key('HOME') else ''
        possibleChoices = [
         os.path.join(ANDROID_HOME, 'platform-tools', adb),
         os.path.join(HOME, 'android', 'platform-tools', adb),
         os.path.join(HOME, 'android-sdk', 'platform-tools', adb)]
        if osName.startswith('Windows'):
            possibleChoices.append(os.path.join('C:\\Program Files\\Android\x07ndroid-sdk\\platform-tools', adb))
            possibleChoices.append(os.path.join('C:\\Program Files (x86)\\Android\x07ndroid-sdk\\platform-tools', adb))
        else:
            if osName.startswith('Linux'):
                possibleChoices.append(os.path.join(os.sep, 'opt', 'android-sdk-linux', 'platform-tools', adb))
                possibleChoices.append(os.path.join(HOME, 'opt', 'android-sdk-linux', 'platform-tools', adb))
                possibleChoices.append(os.path.join(HOME, 'android-sdk-linux', 'platform-tools', adb))
                possibleChoices.append(os.path.join(HOME, 'Android', 'Sdk', 'platform-tools', adb))
            else:
                if osName.startswith('Mac'):
                    possibleChoices.append(os.path.join(HOME, 'Library', 'Android', 'sdk', 'platform-tools', adb))
                    possibleChoices.append(os.path.join(os.sep, 'opt', 'android-sdk-mac_x86', 'platform-tools', adb))
                    possibleChoices.append(os.path.join(HOME, 'opt', 'android-sdk-mac', 'platform-tools', adb))
                    possibleChoices.append(os.path.join(HOME, 'android-sdk-mac', 'platform-tools', adb))
                    possibleChoices.append(os.path.join(HOME, 'opt', 'android-sdk-mac_x86', 'platform-tools', adb))
                    possibleChoices.append(os.path.join(HOME, 'android-sdk-mac_x86', 'platform-tools', adb))
                possibleChoices.append(adb)
                checkedFiles = []
                for exeFile in possibleChoices:
                    checkedFiles.append(exeFile)
                    if not FORCE_FAIL and os.access(exeFile, os.X_OK):
                        return exeFile

            for path in os.environ['PATH'].split(os.pathsep):
                exeFile = os.path.join(path, adb)
                checkedFiles.append(exeFile)
                if not FORCE_FAIL and exeFile is not None and os.access(exeFile, (isWindows or os).X_OK if 1 else os.F_OK):
                    return exeFile

        if not os.environ.has_key('ANDROID_HOME'):
            helpMsg = 'Did you forget to set ANDROID_HOME in the environment?'
        else:
            helpMsg = ''
        raise Exception('adb="%s" is not executable. %s\n\nThese files we unsuccessfully checked to find a suitable \'%s\' executable:\n    %s\n    ' % (adb, helpMsg, adb, ('\n    ').join(checkedFiles)))
        return


def profileStart():
    global profile
    import cProfile
    profile = cProfile.Profile()
    profile.enable()


def profileEnd():
    profile.disable()
    import StringIO, pstats, sys
    s = StringIO.StringIO()
    ps = pstats.Stats(profile, stream=s).sort_stats('cumulative')
    ps.print_stats()
    print >> sys.stderr, '.' * 60
    print >> sys.stderr, 'STATS:\n', s.getvalue()
    print >> sys.stderr, '.' * 60


def debugArgsToDict(a):
    """
    Converts a string representation of debug arguments to a dictionary.
    The string can be of the form

       IDENTIFIER1=val1,IDENTIFIER2=val2

     :param a: the argument string
     :return: the dictionary

    """
    s = a.replace('+', ' ')
    s = s.replace('=', ':')
    s = re.sub('([A-Z][A-Z_]+)', "'\\1'", s)
    return ast.literal_eval('{ ' + s + ' }')
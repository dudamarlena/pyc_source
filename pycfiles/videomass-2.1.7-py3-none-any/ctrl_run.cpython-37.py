# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_sys/ctrl_run.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 6826 bytes
import sys, os, shutil, platform
WORKdir = os.getcwd()
USERName = os.path.expanduser('~')
OS = platform.system()
if OS == 'Windows':
    bpath = '\\AppData\\Roaming\\videomass\\videomassWin32.conf'
    FILEconf = os.path.join(USERName + bpath)
    DIRconf = os.path.join(USERName + '\\AppData\\Roaming\\videomass')
    LOGdir = os.path.join(DIRconf, 'log')
    CACHEdir = os.path.join(DIRconf, 'cache')
else:
    if OS == 'Darwin':
        bpath = 'Library/Application Support/videomass/videomass.conf'
        FILEconf = os.path.join(USERName, bpath)
        DIRconf = os.path.join(USERName, os.path.dirname(bpath))
        LOGdir = os.path.join(USERName, 'Library/Logs/videomass')
        CACHEdir = os.path.join(USERName, 'Library/Caches/videomass')
    else:
        bpath = '.config/videomass/videomass.conf'
        FILEconf = os.path.join(USERName, bpath)
        DIRconf = os.path.join(USERName, '.config/videomass')
        LOGdir = os.path.join(USERName, '.local/share/videomass/log')
        CACHEdir = os.path.join(USERName, '.cache/videomass')

def parsing_fileconf():
    """
    Make a parsing of the configuration file and return
    object list with the current program settings data.
    """
    with open(FILEconf, 'r') as (f):
        fconf = f.readlines()
    lst = [line.strip() for line in fconf if not line.startswith('#')]
    dataconf = [x for x in lst if x]
    if not dataconf:
        return
    return dataconf


def system_check():
    """
    assigning shared data paths and
    checking the configuration folder
    """
    if os.path.isdir('%s/art' % WORKdir):
        localepath = 'locale'
        SRCpath = '%s/share' % WORKdir
        IS_LOCAL = True
    else:
        if OS == 'Windows':
            dirname = os.path.dirname(sys.executable)
            pythonpath = os.path.join(dirname, 'Script', 'videomass')
            localepath = os.path.join(dirname, 'share', 'locale')
            SRCpath = os.path.join(dirname, 'share', 'videomass', 'config')
            IS_LOCAL = False
        else:
            binarypath = shutil.which('videomass')
            if binarypath == '/usr/local/bin/videomass':
                localepath = '/usr/local/share/locale'
                SRCpath = '/usr/local/share/videomass/config'
                IS_LOCAL = False
            else:
                if binarypath == '/usr/bin/videomass':
                    localepath = '/usr/share/locale'
                    SRCpath = '/usr/share/videomass/config'
                    IS_LOCAL = False
                else:
                    import site
                    userbase = site.getuserbase()
                    localepath = userbase + '/share/locale'
                    SRCpath = userbase + '/share/videomass/config'
                    IS_LOCAL = False
    copyerr = False
    existfileconf = True
    if os.path.exists(DIRconf):
        if os.path.isfile(FILEconf):
            DATAconf = parsing_fileconf()
            if not DATAconf:
                print('The file configuration is damaged! try to restore..')
                existfileconf = False
            if float(DATAconf[0]) != 2.0:
                existfileconf = False
    else:
        existfileconf = False
    if not existfileconf:
        try:
            if OS == 'Windows':
                shutil.copyfile('%s/videomassWin32.conf' % SRCpath, FILEconf)
            else:
                shutil.copyfile('%s/videomass.conf' % SRCpath, FILEconf)
            DATAconf = parsing_fileconf()
        except IOError as e:
            try:
                copyerr = e
                DATAconf = None
            finally:
                e = None
                del e

    if not os.path.exists(os.path.join(DIRconf, 'presets')):
        try:
            shutil.copytree(os.path.join(SRCpath, 'presets'), os.path.join(DIRconf, 'presets'))
        except (OSError, IOError) as e:
            try:
                copyerr = e
                DATAconf = None
            finally:
                e = None
                del e

    else:
        try:
            shutil.copytree(SRCpath, DIRconf)
            DATAconf = parsing_fileconf()
        except (OSError, IOError) as e:
            try:
                copyerr = e
                DATAconf = None
            finally:
                e = None
                del e

        return (
         OS,
         SRCpath,
         copyerr,
         IS_LOCAL,
         DATAconf,
         localepath,
         FILEconf,
         WORKdir,
         DIRconf,
         LOGdir,
         CACHEdir)
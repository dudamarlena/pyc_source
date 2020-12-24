# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.6/site-packages/apptool/backup.py
# Compiled at: 2010-10-09 01:07:17
import os, sys, pwd, shutil, common, cli
home = common.mainWorkDir()

def generateTextInfo():
    a = os.linesep.join(os.listdir(os.path.join(home, 'Apps', 'app')))
    p = os.linesep.join(os.listdir(os.path.join(home, 'Apps', 'app-private')))
    try:
        f = open(os.path.join(home, 'BACKUP_INFO'), 'w')
        try:
            f.write('Thanks for using AppTool!' + os.linesep + os.linesep + '=' * 60 + os.linesep + os.linesep + 'Backed up apps:' + os.linesep + os.linesep + a + p + os.linesep + os.linesep + '=' * 60)
        except (IOError, OSError), e:
            cli.warning(str(e))

    finally:
        f.close()


def backupApps():
    try:
        if os.path.isdir(home):
            shutil.rmtree(home)
        os.makedirs(home)
        cli.message('Attempting to pull apps from device')
        common.adbPull(os.path.join(home, 'Apps'))
        cli.message('Generating text information')
        generateTextInfo()
        filename = '%s_AppBackup.zip' % pwd.getpwuid(os.getuid()).pw_name
        cli.message('Compressing backed up apps')
        mkzip = common.ZipUtil(zipwrite=True, zipname=os.path.join(home, filename))
        mkzip.work()
        if os.path.isfile(os.path.join(home, filename)):
            cli.success('Apps backed up successfully')
            shutil.rmtree(os.path.join(home, 'Apps'))
        else:
            cli.error('Backup failed')
    except:
        cli.warning('Aborting...')
        shutil.rmtree(home)
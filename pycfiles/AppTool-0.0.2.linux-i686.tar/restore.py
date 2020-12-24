# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/apptool/restore.py
# Compiled at: 2010-10-09 01:07:17
import os, pwd, shutil, common, cli

def restoreApps():
    try:
        home = common.mainWorkDir()
        filename = '%s_AppBackup.zip' % pwd.getpwuid(os.getuid()).pw_name
        if not os.path.isdir(home):
            return cli.error("AppTool directory not found, have you ran the `backup' option?")
        if not os.path.isfile(os.path.join(home, filename)):
            return cli.error('No backed up apps were found!')
        cli.message('Uncompressing previous backed up apps')
        os.chdir(home)
        exzip = common.ZipUtil(zipextract=True, zipname=filename)
        exzip.work()
        cli.message('Attempting to reinstall apps')
        for apk in os.listdir(os.path.join(home, 'app')):
            if apk:
                common.adbInstall(os.path.join(home, 'app', apk))

        for apk in os.listdir(os.path.join(home, 'app-private')):
            if apk:
                common.adbInstall(os.path.join(home, 'app-private', apk))

        cli.success('Done restoring')
        shutil.rmtree(os.path.join(home, 'Apps'))
    except:
        cli.warning('Aborting...')
        if os.path.isdir(os.path.join(home, 'app')):
            shutil.rmtree(os.path.join(home, 'app'))
        if os.path.isdir(os.path.join(home, 'app-private')):
            shutil.rmtree(os.path.join(home, 'app-private'))
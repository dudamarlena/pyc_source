# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/fftool/firefox_run.py
# Compiled at: 2016-05-10 00:59:47
from outlawg import Outlawg
from fftool import DIR_CONFIGS, local
from firefox_env_handler import IniHandler
Log = Outlawg()
env = IniHandler()
env.load_os_config(DIR_CONFIGS)

def launch_firefox(profile_path, channel):
    """relies on the other functions (download, install, profile)
    having completed.
    """
    FIREFOX_APP_BIN = env.get(channel, 'PATH_FIREFOX_BIN_ENV')
    Log.header('LAUNCH FIREFOX')
    print ('Launching Firefox {0} with profile: {1}').format(channel, profile_path)
    cmd = ('"{0}" -profile "{1}"').format(FIREFOX_APP_BIN, profile_path)
    print 'CMD: ' + cmd
    local(cmd)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/fftool/firefox_download.py
# Compiled at: 2016-05-10 00:59:16
"""Module to download OS-specific versions of Firefox:
1. Nightly (nightly)
2. Developer Edition (aurora)
3. Beta (beta)
4. General Release (release)
"""
import os, time, ConfigParser as configparser
from outlawg import Outlawg
from fftool import DIR_TEMP_BROWSERS as BASE_DIR, DIR_CONFIGS
from firefox_install import install, get_firefox_version
from firefox_env_handler import IniHandler
from mozdownload import FactoryScraper
env = IniHandler()
env.load_os_config(DIR_CONFIGS)
CONFIG_CHANNELS = os.path.join(DIR_CONFIGS, 'channels.ini')
SCRIPT_START_TIME = time.time()
config = configparser.ConfigParser()
config.read(CONFIG_CHANNELS)
Log = Outlawg()

def modification_date(filename):
    return os.path.getmtime(filename)


def download(channel):
    Log.header('DOWNLOAD FIREFOX')
    ch_type = config.get(channel, 'type')
    ch_version = config.get(channel, 'version')
    ch_branch = config.get(channel, 'branch')
    ch_platform = env.get(channel, 'PLATFORM')
    download_filename = env.get(channel, 'DOWNLOAD_FILENAME')
    download_path = os.path.join(BASE_DIR, download_filename)
    args = {'channel': channel, 'download_path': download_path}
    print ('Downloading {channel} to {download_path}').format(**args)
    scraper = FactoryScraper(ch_type, version=ch_version, branch=ch_branch, destination=download_path, platform=ch_platform)
    scraper.download()
    is_recent_file = modification_date(download_path) > SCRIPT_START_TIME
    firefox_bin = env.get(channel, 'PATH_FIREFOX_BIN_ENV')
    if is_recent_file or not os.path.exists(firefox_bin):
        install(channel)
    else:
        firefox_version = get_firefox_version(channel)
        args = {'channel': channel, 'version': firefox_version}
        msg = 'You have the latest version of {channel} installed ({version}).'
        Log.header('BROWSER VERSION')
        print msg.format(**args)


def download_all():
    for channel in config.sections():
        download(channel)
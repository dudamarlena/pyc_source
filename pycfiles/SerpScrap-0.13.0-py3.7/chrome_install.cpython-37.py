# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\serpscrap\chrome_install.py
# Compiled at: 2018-08-26 07:33:12
# Size of source mod 2**32: 2967 bytes
from scrapcore.logger import Logger
import os, platform, stat, subprocess, tempfile, urllib.request, zipfile
logger = Logger()
logger.setup_logger()
logger = logger.get_logger()

class ChromeInstall:
    home_dir = os.path.expanduser('chromedriver/')
    binary_win = 'chromedriver.exe'
    binary_linux = 'chromedriver'
    binary_mac64 = 'chromedriver'

    def get_os(self):
        return platform.system()

    def detect_chromedriver(self):
        logger.info('detecting chromedriver')
        this_os = self.get_os().lower()
        if 'windows' in this_os:
            if os.path.isfile(self.home_dir + self.binary_win):
                os.chmod(self.home_dir + self.binary_win, 755)
                return self.home_dir + self.binary_win
        elif 'linux' in this_os:
            if os.path.isfile(self.home_dir + self.binary_linux):
                os.chmod(self.home_dir + self.binary_linux, 755)
                return self.home_dir + self.binary_linux
        elif 'darwin' in this_os:
            if os.path.isfile(self.home_dir + self.binary_mac64):
                os.chmod(self.home_dir + self.binary_mac64, 755)
                return self.home_dir + self.binary_mac64
        else:
            raise Exception('\n            Platform not supported.\n            install chromedriver by your own and update the path in your config\n            ')

    def download(self):
        logger.info('downloading chromedriver')
        this_os = self.get_os().lower()
        base_url = 'http://chromedriver.storage.googleapis.com/2.41/'
        if 'windows' in this_os:
            file_name = 'chromedriver_win32.zip'
            archive = 'zip'
        else:
            if 'linux' in this_os:
                os.chmod('install_chrome.sh', 755 | stat.S_IEXEC)
                subprocess.call('install_chrome.sh')
                archive = 'zip'
                file_name = 'chromedriver_linux64.zip'
            else:
                if 'darwin' in this_os:
                    file_name = 'chromedriver_mac64.zip'
                    archive = 'zip'
                else:
                    raise Exception('\n            Platform not supported.\n            install chromedriver by your own and update the path in your config\n            ')
        tmp_dir = tempfile.gettempdir() + '/'
        try:
            urllib.request.urlretrieve(base_url + file_name, tmp_dir + file_name)
            self.unpack(tmp_dir + file_name, archive)
        except:
            raise Exception('Download and unpack of chromedriver failed. Check if %(tmp_dir)s exists and has write permissions' % {'tmp_dir': tmp_dir})

    def unpack(self, file_path, archive):
        logger.info('unpacking chromedriver')
        if os.path.isdir(self.home_dir) is False:
            os.mkdir(self.home_dir)
        if 'zip' in archive:
            with zipfile.ZipFile(file_path, 'r') as (zip_ref):
                zip_ref.extractall(self.home_dir)
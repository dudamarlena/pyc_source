# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/youtubedlupdater.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 6386 bytes
import subprocess, shutil, ssl, urllib.request, wx
from pubsub import pub
from threading import Thread
get = wx.GetApp()
OS = get.OS

class CheckNewRelease(Thread):
    __doc__ = '\n    Read the latest version of youtube-dl on github website (see url) .\n    '

    def __init__(self, url):
        """
        Attributes defined here:
        self.data: tuple object with exit status of the process
        """
        Thread.__init__(self)
        self.url = url
        self.data = None
        self.start()

    def run(self):
        """
        Check for new version release
        """
        ssl._create_default_https_context = ssl._create_unverified_context
        try:
            req = urllib.request.build_opener().open(self.url).read().decode('utf-8').strip()
            self.data = (req, None)
        except urllib.error.HTTPError as error:
            try:
                self.data = (
                 None, error)
            finally:
                error = None
                del error

        except urllib.error.URLError as error:
            try:
                self.data = (
                 None, error)
            finally:
                error = None
                del error

        wx.CallAfter((pub.sendMessage), 'RESULT_EVT',
          status='')


class Command_Execution(Thread):
    __doc__ = '\n    Executes generic command line with an executable, e.g.\n    - read the installed version of youtube-dl\n    - update the downloaded sources of youtube-dl\n    '

    def __init__(self, cmd):
        """
        OS: Operative System id
        self.cmd: command line list object
        self.status: tuple object with exit status of the process
        self.data: returned output of the self.status
        """
        Thread.__init__(self)
        self.cmd = cmd
        self.data = None
        self.status = None
        self.start()

    def run(self):
        """
        Execute command line via subprocess class and get output
        at the end of the process.
        """
        if OS == 'Windows':
            cmd = ' '.join(self.cmd)
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            cmd = self.cmd
            info = None
        try:
            p = subprocess.Popen(cmd, stdout=(subprocess.PIPE),
              stderr=(subprocess.STDOUT),
              universal_newlines=True,
              startupinfo=info)
            out = p.communicate()
        except (OSError, FileNotFoundError) as oserr:
            try:
                self.status = (
                 '%s' % oserr, 'error')
            finally:
                oserr = None
                del oserr

        else:
            if p.returncode and not out[0]:
                if not out[1]:
                    if OS == 'Windows':
                        self.status = _('Requires MSVCR100.dll\nTo resolve this problem install: Microsoft Visual C++ 2010 Redistributable Package (x86)', 'error')
                else:
                    self.status = (
                     out[0], 'error')
            else:
                self.status = (
                 out[0], out[1])
            wx.CallAfter((pub.sendMessage), 'RESULT_EVT',
              status='')


class Upgrade_Latest(Thread):
    __doc__ = '\n    Download latest version of youtube-dl.exe, see self.url .\n    '

    def __init__(self, url, dest):
        """
        Attributes defined here:
        latest: latest version available .
        self.dest: location pathname to download
        self.data: returned output of the self.status
        self.status: tuple object with exit status of the process

        """
        Thread.__init__(self)
        self.url = url
        self.dest = dest
        self.data = None
        self.status = None
        self.start()

    def run(self):
        """
        Check for new version release
        """
        context = ssl._create_unverified_context()
        try:
            with urllib.request.urlopen((self.url), context=context) as (response):
                with open(self.dest, 'wb') as (out_file):
                    shutil.copyfileobj(response, out_file)
            self.status = (
             self.url, None)
        except urllib.error.HTTPError as error:
            try:
                self.status = (
                 None, error)
            finally:
                error = None
                del error

        except urllib.error.URLError as error:
            try:
                self.status = (
                 None, error)
            finally:
                error = None
                del error

        self.data = self.status
        wx.CallAfter((pub.sendMessage), 'RESULT_EVT',
          status='')
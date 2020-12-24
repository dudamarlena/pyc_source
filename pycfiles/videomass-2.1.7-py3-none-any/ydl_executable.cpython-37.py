# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/ydl_executable.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 9816 bytes
import wx, subprocess, os
from threading import Thread
import time
from pubsub import pub
get = wx.GetApp()
OS = get.OS
LOGDIR = get.LOGdir
FFMPEG_URL = get.FFMPEG_url
execYdl = get.execYdl
if not OS == 'Windows':
    import shlex
    linemsg = _('Unrecognized error')
else:
    if os.path.isfile(execYdl):
        linemsg = _('\nRequires MSVCR100.dll\nTo resolve this problem install: Microsoft Visual C++ 2010 Redistributable Package (x86)')
    else:
        linemsg = _('Unrecognized error')
executable_not_found_msg = _("Is 'youtube-dl' installed on your system?")

def logWrite(cmd, sterr, logname):
    """
    writes youtube-dl commands and status error during
    threads below
    """
    if sterr:
        apnd = '...%s\n\n' % sterr
    else:
        apnd = '%s\n\n' % cmd
    with open(os.path.join(LOGDIR, logname), 'a') as (log):
        log.write(apnd)


class Ydl_DL_Exec(Thread):
    __doc__ = '\n    Ydl_DL_Exec represents a separate thread for running\n    youtube-dl executable with subprocess class and capturing its\n    stdout/stderr output in real time .\n    '

    def __init__(self, varargs, logname):
        """
        Attributes defined here:
        self.stop_work_thread:  process terminate value
        self.urls:          urls list
        self.opt:           option strings to adding
        self.outtmpl:       options template to renaming on pathname
        self.outputdir:     pathname destination
        self.count:         increases with the progressive account elements
        self.countmax:      length of self.urls
        self.logname:       title log name for logging

        """
        Thread.__init__(self)
        self.stop_work_thread = False
        self.urls = varargs[1]
        self.opt = varargs[4][0]
        self.outtmpl = varargs[4][1]
        self.outputdir = varargs[3]
        self.count = 0
        self.countmax = len(varargs[1])
        self.logname = logname
        self.start()

    def run(self):
        """
        Subprocess initialize thread.
        """
        ssl = '--no-check-certificate' if OS == 'Windows' else ''
        for url in self.urls:
            cmd = '"{0}" {1} --newline --ignore-errors -o "{2}/{3}" {4} --ignore-config --restrict-filenames "{5}" --ffmpeg-location "{6}"'.format(execYdl, ssl, self.outputdir, self.outtmpl, self.opt, url, FFMPEG_URL)
            self.count += 1
            count = 'URL %s/%s' % (self.count, self.countmax)
            com = '%s\n%s' % (count, cmd)
            wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
              count=count,
              duration=100,
              fname=url,
              end='')
            logWrite(com, '', self.logname)
            if not OS == 'Windows':
                cmd = shlex.split(cmd)
                info = None
            else:
                info = subprocess.STARTUPINFO()
                info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            try:
                with subprocess.Popen(cmd, stdout=(subprocess.PIPE),
                  stderr=(subprocess.STDOUT),
                  bufsize=1,
                  universal_newlines=True,
                  startupinfo=info) as (p):
                    for line in p.stdout:
                        wx.CallAfter((pub.sendMessage), 'UPDATE_YDL_EXECUTABLE_EVT',
                          output=line,
                          duration=100,
                          status=0)
                        if self.stop_work_thread:
                            p.terminate()
                            break

                    if p.wait():
                        if 'line' not in locals():
                            line = linemsg
                        wx.CallAfter((pub.sendMessage), 'UPDATE_YDL_EXECUTABLE_EVT',
                          output=line,
                          duration=100,
                          status=(p.wait()))
                        logWrite('', 'Exit status: %s' % p.wait(), self.logname)
                    else:
                        wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
                          count='',
                          duration='',
                          fname='',
                          end='ok')
            except (OSError, FileNotFoundError) as err:
                try:
                    e = '%s\n  %s' % (err, executable_not_found_msg)
                    wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
                      count=e,
                      duration=0,
                      fname=url,
                      end='error')
                    break
                finally:
                    err = None
                    del err

            if self.stop_work_thread:
                p.terminate()
                break

        time.sleep(0.5)
        wx.CallAfter(pub.sendMessage, 'END_EVT')

    def stop(self):
        """
        Sets the stop work thread to terminate the process
        """
        self.stop_work_thread = True


class Ydl_EI_Exec(Thread):
    __doc__ = "\n    Ydl_EI_Exec it is a separate thread to run youtube-dl executable\n    with subprocess class to get -at the end of the process- 'Format\n    code' data and exit status from stdout/stderr output .\n    "

    def __init__(self, url):
        """
        self.urls:          urls list
        """
        Thread.__init__(self)
        self.url = url
        self.status = None
        self.data = None
        self.start()

    def run(self):
        """
        Subprocess initialize thread.
        """
        ssl = '--no-check-certificate' if OS == 'Windows' else ''
        cmd = '"{0}" {1} --newline --ignore-errors --ignore-config --restrict-filenames -F "{2}"'.format(execYdl, ssl, self.url)
        if not OS == 'Windows':
            cmd = shlex.split(cmd)
            info = None
        else:
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        try:
            p = subprocess.Popen(cmd, stdout=(subprocess.PIPE),
              stderr=(subprocess.STDOUT),
              universal_newlines=True,
              startupinfo=info)
            out = p.communicate()
        except OSError as oserr:
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
                        self.status = (
                         linemsg, 'error')
                else:
                    self.status = (
                     out[0], 'error')
            else:
                self.status = (
                 out[0], out[1])
            wx.CallAfter((pub.sendMessage), 'RESULT_EVT',
              status='')
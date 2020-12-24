# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/picture_exporting.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 6540 bytes
import wx, subprocess, os
from threading import Thread
import time
from pubsub import pub
get = wx.GetApp()
OS = get.OS
LOGDIR = get.LOGdir
FFMPEG_URL = get.FFMPEG_url
FFMPEG_LOGLEV = get.FFMPEG_loglev
if not OS == 'Windows':
    import shlex
not_exist_msg = _("Is 'ffmpeg' installed on your system?")

def logWrite(cmd, sterr, logname):
    """
    writes ffmpeg commands and status error during threads below
    """
    if sterr:
        apnd = '...%s\n\n' % sterr
    else:
        apnd = '%s\n\n' % cmd
    with open(os.path.join(LOGDIR, logname), 'a') as (log):
        log.write(apnd)


class PicturesFromVideo(Thread):
    __doc__ = '\n    This class represents a separate thread for running simple\n    single processes to save video sequences as pictures.\n    '

    def __init__(self, varargs, duration, logname, timeseq):
        """
        self.cmd contains a unique string that comprend filename input
        and filename output also.
        The duration adds another 10 seconds due to problems with the
        progress bar
        """
        Thread.__init__(self)
        self.stop_work_thread = False
        self.cmd = varargs[4]
        self.duration = duration[0] + 10
        self.time_seq = timeseq
        self.count = 0
        self.logname = logname
        self.fname = varargs[1]
        self.start()

    def run(self):
        """
        Subprocess initialize thread.
        """
        cmd = '%s %s %s -i "%s" %s ' % (FFMPEG_URL,
         self.time_seq,
         FFMPEG_LOGLEV,
         self.fname,
         self.cmd)
        count = 'File %s/%s' % ('1', '1')
        com = '%s\n%s' % (count, cmd)
        wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
          count=count,
          duration=(self.duration),
          fname=(self.fname),
          end='')
        logWrite(com, '', self.logname)
        if not OS == 'Windows':
            cmd = shlex.split(cmd)
            info = None
        else:
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        try:
            with subprocess.Popen(cmd, stderr=(subprocess.PIPE),
              bufsize=1,
              universal_newlines=True,
              startupinfo=info) as (p):
                for line in p.stderr:
                    wx.CallAfter((pub.sendMessage), 'UPDATE_EVT',
                      output=line,
                      duration=(self.duration),
                      status=0)
                    if self.stop_work_thread:
                        p.terminate()
                        break

                if p.wait():
                    wx.CallAfter((pub.sendMessage), 'UPDATE_EVT',
                      output=line,
                      duration=(self.duration),
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
                e = '%s\n  %s' % (err, not_exist_msg)
                wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
                  count=e,
                  duration=0,
                  fname=(self.fname),
                  end='error')
            finally:
                err = None
                del err

        time.sleep(0.5)
        wx.CallAfter(pub.sendMessage, 'END_EVT')

    def stop(self):
        """
        Sets the stop work thread to terminate the process
        """
        self.stop_work_thread = True
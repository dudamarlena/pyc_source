# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/two_pass.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 11302 bytes
import wx, subprocess, itertools, os
from threading import Thread
import time
from pubsub import pub
get = wx.GetApp()
OS = get.OS
LOGDIR = get.LOGdir
FFMPEG_URL = get.FFMPEG_url
FFMPEG_LOGLEV = get.FFMPEG_loglev
FF_THREADS = get.FFthreads
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


class TwoPass(Thread):
    __doc__ = '\n    This class represents a separate thread which need to read the\n    stdout/stderr in real time mode. The subprocess module is instantiated\n    twice for two different tasks: the process on the first video pass and\n    the process on the second video pass for video only.\n    '

    def __init__(self, varargs, duration, logname, timeseq):
        """
        The 'volume' attribute may have an empty value, but it will
        have no influence on the type of conversion.
        """
        Thread.__init__(self)
        self.stop_work_thread = False
        self.filelist = varargs[1]
        self.passList = varargs[5]
        self.outputdir = varargs[3]
        self.extoutput = varargs[2]
        self.duration = duration
        self.time_seq = timeseq
        self.volume = varargs[7]
        self.count = 0
        self.countmax = len(varargs[1])
        self.logname = logname
        self.nul = 'NUL' if OS == 'Windows' else '/dev/null'
        self.start()

    def run(self):
        """
        Subprocess initialize thread.
        """
        for files, folders, volume, duration in itertools.zip_longest((self.filelist), (self.outputdir),
          (self.volume),
          (self.duration),
          fillvalue=''):
            basename = os.path.basename(files)
            filename = os.path.splitext(basename)[0]
            source_ext = os.path.splitext(basename)[1].split('.')[1]
            outext = source_ext if not self.extoutput else self.extoutput
            pass1 = '%s %s %s -i "%s" %s %s -y %s' % (
             FFMPEG_URL,
             FFMPEG_LOGLEV,
             self.time_seq,
             files,
             self.passList[0],
             FF_THREADS,
             self.nul)
            self.count += 1
            count = 'File %s/%s - Pass One' % (self.count, self.countmax)
            cmd = '%s\n%s' % (count, pass1)
            wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
              count=count,
              duration=duration,
              fname=files,
              end='')
            logWrite(cmd, '', self.logname)
            if not OS == 'Windows':
                pass1 = shlex.split(pass1)
                info = None
            else:
                info = subprocess.STARTUPINFO()
                info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            try:
                with subprocess.Popen(pass1, stderr=(subprocess.PIPE),
                  bufsize=1,
                  universal_newlines=True,
                  startupinfo=info) as (p1):
                    for line in p1.stderr:
                        wx.CallAfter((pub.sendMessage), 'UPDATE_EVT',
                          output=line,
                          duration=duration,
                          status=0)
                        if self.stop_work_thread:
                            p1.terminate()
                            break

                    if p1.wait():
                        wx.CallAfter((pub.sendMessage), 'UPDATE_EVT',
                          output=line,
                          duration=duration,
                          status=(p1.wait()))
                        logWrite('', 'Exit status: %s' % p1.wait(), self.logname)
            except (OSError, FileNotFoundError) as err:
                try:
                    e = '%s\n  %s' % (err, not_exist_msg)
                    wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
                      count=e,
                      duration=0,
                      fname=files,
                      end='error')
                    break
                finally:
                    err = None
                    del err

            if self.stop_work_thread:
                p1.terminate()
                break
            else:
                if p1.wait() == 0:
                    wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
                      count='',
                      duration='',
                      fname='',
                      end='ok')
                pass2 = '%s %s %s -i "%s" %s %s %s -y "%s/%s.%s"' % (
                 FFMPEG_URL,
                 FFMPEG_LOGLEV,
                 self.time_seq,
                 files,
                 self.passList[1],
                 volume,
                 FF_THREADS,
                 folders,
                 filename,
                 outext)
                count = 'File %s/%s - Pass Two' % (self.count, self.countmax)
                cmd = '%s\n%s' % (count, pass2)
                wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
                  count=count,
                  duration=duration,
                  fname=files,
                  end='')
                logWrite(cmd, '', self.logname)
                if not OS == 'Windows':
                    pass2 = shlex.split(pass2)
                    info = None
                else:
                    info = subprocess.STARTUPINFO()
                info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            with subprocess.Popen(pass2, stderr=(subprocess.PIPE),
              bufsize=1,
              universal_newlines=True,
              startupinfo=info) as (p2):
                for line2 in p2.stderr:
                    wx.CallAfter((pub.sendMessage), 'UPDATE_EVT',
                      output=line2,
                      duration=duration,
                      status=0)
                    if self.stop_work_thread:
                        p2.terminate()
                        break

                if p2.wait():
                    wx.CallAfter((pub.sendMessage), 'UPDATE_EVT',
                      output=line,
                      duration=duration,
                      status=(p2.wait()))
                    logWrite('', 'Exit status: %s' % p2.wait(), self.logname)
            if self.stop_work_thread:
                p2.terminate()
                break
            if p2.wait() == 0:
                wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
                  count='',
                  duration='',
                  fname='',
                  end='ok')

        time.sleep(0.5)
        wx.CallAfter(pub.sendMessage, 'END_EVT')

    def stop(self):
        """
        Sets the stop work thread to terminate the process
        """
        self.stop_work_thread = True
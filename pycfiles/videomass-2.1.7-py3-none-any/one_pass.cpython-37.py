# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/one_pass.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 8294 bytes
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


class OnePass(Thread):
    __doc__ = '\n    This class represents a separate thread for running processes,\n    which need to read the stdout/stderr in real time.\n    '

    def __init__(self, varargs, duration, logname, timeseq):
        """
        Some attribute can be empty, this depend from conversion type.
        If the format/container is not changed on a conversion, the
        'extoutput' attribute will have an empty value.
        The 'volume' attribute may also have an empty value, but it will
        have no influence on the type of conversion.
        """
        Thread.__init__(self)
        self.stop_work_thread = False
        self.filelist = varargs[1]
        self.command = varargs[4]
        self.outputdir = varargs[3]
        self.extoutput = varargs[2]
        self.duration = duration
        self.volume = varargs[7]
        self.count = 0
        self.countmax = len(varargs[1])
        self.logname = logname
        self.time_seq = timeseq
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
            cmd = '%s %s %s -i "%s" %s %s %s -y "%s/%s.%s"' % (
             FFMPEG_URL,
             self.time_seq,
             FFMPEG_LOGLEV,
             files,
             self.command,
             volume,
             FF_THREADS,
             folders,
             filename,
             outext)
            self.count += 1
            count = 'File %s/%s' % (self.count, self.countmax)
            com = '%s\n%s' % (count, cmd)
            wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
              count=count,
              duration=duration,
              fname=files,
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
                          duration=duration,
                          status=0)
                        if self.stop_work_thread:
                            p.terminate()
                            break

                    if p.wait():
                        wx.CallAfter((pub.sendMessage), 'UPDATE_EVT',
                          output=line,
                          duration=duration,
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
                      fname=files,
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
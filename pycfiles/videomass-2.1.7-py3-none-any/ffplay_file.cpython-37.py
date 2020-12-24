# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/ffplay_file.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 5308 bytes
import wx, subprocess, os
from threading import Thread
from videomass3.vdms_io.make_filelog import write_log
get = wx.GetApp()
LOGDIR = get.LOGdir
FFPLAY_URL = get.FFPLAY_url
ffplay_loglev = get.FFPLAY_loglev
OS = get.OS
if not OS == 'Windows':
    import shlex

def msg_Error(msg):
    """
    Receive error messages via wxCallafter
    """
    wx.MessageBox('FFplay ERROR:  %s' % msg, 'Videomass: FFplay', wx.ICON_ERROR)


def msg_Info(msg):
    """
    Receive info messages via wxCallafter
    """
    wx.MessageBox('FFplay INFORMATION:  %s' % msg, 'Videomass: FFplay', wx.ICON_INFORMATION)


class File_Play(Thread):
    __doc__ = '\n    Simple multimedia playback with subprocess.Popen class to run ffplay\n    by FFmpeg (ffplay is a player which need x-window-terminal-emulator)\n    '

    def __init__(self, filepath, timeseq, param):
        """
        The self.FFPLAY_loglevel has flag 'error -hide_banner'
        by default (see videomass.conf).
        NOTE: Do not use '-stats' option it do not work.
        """
        Thread.__init__(self)
        self.filename = filepath
        self.time_seq = timeseq
        self.param = param
        self.logf = os.path.join(LOGDIR, 'Videomass_FFplay.log')
        write_log('Videomass_FFplay.log', LOGDIR)
        self.start()

    def run(self):
        """
        Get and redirect output errors on p.returncode instance and on
        OSError exception. Otherwise the getted output as information
        given by error [1] .
        """
        cmd = '%s %s %s -i "%s" %s' % (FFPLAY_URL,
         self.time_seq,
         ffplay_loglev,
         self.filename,
         self.param)
        self.logWrite(cmd)
        if not OS == 'Windows':
            cmd = shlex.split(cmd)
            info = None
            shell = False
        else:
            shell = True
            info = None
        try:
            p = subprocess.Popen(cmd, shell=shell,
              stderr=(subprocess.PIPE),
              universal_newlines=True,
              startupinfo=info)
            error = p.communicate()
        except OSError as err:
            try:
                wx.CallAfter(msg_Error, err)
                self.logError(err)
                return
            finally:
                err = None
                del err

        else:
            if p.returncode:
                if error[1]:
                    msg = error[1]
                else:
                    msg = 'Unrecognized error'
                wx.CallAfter(msg_Error, error[1])
                self.logError(error[1])
                return

    def logWrite(self, cmd):
        """
        write ffplay command log
        """
        with open(self.logf, 'a') as (log):
            log.write('%s\n\n' % cmd)

    def logError(self, error):
        """
        write ffplay errors
        """
        with open(self.logf, 'a') as (logerr):
            logerr.write('[FFMPEG] FFplay ERRORS:\n%s\n\n' % error)
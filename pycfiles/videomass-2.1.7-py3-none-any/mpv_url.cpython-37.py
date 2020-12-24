# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/mpv_url.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 4988 bytes
import wx, subprocess, os
from threading import Thread
from videomass3.vdms_io.make_filelog import write_log
get = wx.GetApp()
LOGDIR = get.LOGdir
OS = get.OS
MPV_LINK = get.MPV_url
if not OS == 'Windows':
    import shlex

def msg_Error(msg):
    """
    Receive error messages via wxCallafter
    """
    wx.MessageBox('%s' % msg, 'Videomass: mpv ERROR', wx.ICON_ERROR)


def msg_Info(msg):
    """
    Receive info messages via wxCallafter
    """
    wx.MessageBox('MPV message information:  %s' % msg, 'Videomass: mpv INFORMATION', wx.ICON_INFORMATION)


class Url_Play(Thread):
    __doc__ = '\n    subprocess.Popen class to run mpv media player for playback URLs .\n    '

    def __init__(self, url, quality):
        """
        quality: is flag to set media quality result
        """
        Thread.__init__(self)
        self.url = url
        self.quality = quality
        self.logf = os.path.join(LOGDIR, 'Videomass_mpv.log')
        write_log('Videomass_mpv.log', LOGDIR)
        self.start()

    def run(self):
        """
        Get and redirect output and errors on p.returncode instance and on
        exceptions. Otherwise the getted output as information
        given by output .
        """
        if OS == 'Windows':
            cmd = '%s --ytdl-raw-options=no-check-certificate= %s --ytdl-format=%s %s' % (
             MPV_LINK,
             self.url,
             self.quality,
             self.url)
            shell = False
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.SW_HIDE
        else:
            cmd = '%s --ytdl-format=%s %s' % (MPV_LINK, self.quality, self.url)
            cmd = shlex.split(cmd)
            info = None
            shell = False
        self.logWrite(cmd)
        try:
            p = subprocess.Popen(cmd, shell=shell,
              stdout=(subprocess.PIPE),
              stderr=(subprocess.STDOUT),
              universal_newlines=True,
              startupinfo=info)
            error, output = p.communicate()
        except (OSError, FileNotFoundError) as err:
            try:
                wx.CallAfter(msg_Error, _('{}\n\nYou need mpv to play urls but mpv is not found.').format(err))
                self.logError(err)
                return
            finally:
                err = None
                del err

        else:
            if p.returncode:
                if error:
                    msg = error
                else:
                    msg = 'Unrecognized error'
                wx.CallAfter(msg_Error, error)
                self.logError(error)
                return
            if output:
                wx.CallAfter(msg_Info, output)
                self.logWrite(output)
                return

    def logWrite(self, cmd):
        """
        write mpv command log
        """
        with open(self.logf, 'a') as (log):
            log.write('%s\n\n' % cmd)

    def logError(self, error):
        """
        write mpv errors
        """
        with open(self.logf, 'a') as (logerr):
            logerr.write('[MPV] MESSAGE:\n%s\n\n' % error)
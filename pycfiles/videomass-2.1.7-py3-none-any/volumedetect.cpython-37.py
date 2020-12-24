# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/volumedetect.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 6001 bytes
import wx, os
from pubsub import pub
import subprocess
from threading import Thread
from videomass3.vdms_io.make_filelog import write_log
get = wx.GetApp()
LOGDIR = get.LOGdir
OS = get.OS
FFMPEG_URL = get.FFMPEG_url
if not OS == 'Windows':
    import shlex

class VolumeDetectThread(Thread):
    __doc__ = '\n    This class represents a separate subprocess thread to get\n    audio volume peak level when required for audio normalization\n    process.\n\n    NOTE: all error handling (including verification of the\n    existence of files) is entrusted to ffmpeg, except for the\n    lack of ffmpeg of course.\n    '

    def __init__(self, timeseq, filelist, audiomap, OS):
        """
        Replace /dev/null with NUL on Windows.

        self.status: None, if nothing error,
                     'str error' if errors.
        self.data: it is a tuple containing the list of audio volume
                   parameters and the self.status of the error output,
                   in the form:
                   ([[maxvol, medvol], [etc,etc]], None or "str errors")
        """
        Thread.__init__(self)
        self.filelist = filelist
        self.time_seq = timeseq
        self.audiomap = audiomap
        self.status = None
        self.data = None
        self.nul = 'NUL' if OS == 'Windows' else '/dev/null'
        self.logf = os.path.join(LOGDIR, 'Videomass_volumedected.log')
        write_log('Videomass_volumedected.log', LOGDIR)
        self.start()

    def run(self):
        """
        Audio volume data is getted by the thread's caller using
        the thread.data method (see IO_tools).
        NOTE: wx.callafter(pub...) do not send data to pop-up
              dialog, but a empty string that is useful to get
              the end of the process to close of the pop-up.
        """
        volume = list()
        for files in self.filelist:
            cmd = '{0} {1} -i "{2}" -hide_banner {3} -af volumedetect -vn -sn -dn -f null {4}'.format(FFMPEG_URL, self.time_seq, files, self.audiomap, self.nul)
            self.logWrite(cmd)
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
                output = p.communicate()
            except (OSError, FileNotFoundError) as e:
                try:
                    self.status = e
                    break
                finally:
                    e = None
                    del e

            else:
                if p.returncode:
                    self.status = output[0]
                    break
                else:
                    raw_list = output[0].split()
                if 'mean_volume:' in raw_list:
                    mean_volume = raw_list.index('mean_volume:')
                    medvol = '%s dB' % raw_list[(mean_volume + 1)]
                    max_volume = raw_list.index('max_volume:')
                    maxvol = '%s dB' % raw_list[(max_volume + 1)]
                    volume.append([maxvol, medvol])

        self.data = (
         volume, self.status)
        if self.status:
            self.logError()
        wx.CallAfter((pub.sendMessage), 'RESULT_EVT',
          status='')

    def logWrite(self, cmd):
        """
        write ffmpeg command log
        """
        with open(self.logf, 'a') as (log):
            log.write('%s\n\n' % cmd)

    def logError(self):
        """
        write ffmpeg volumedected errors
        """
        with open(self.logf, 'a') as (logerr):
            logerr.write('[FFMPEG] volumedetect ERRORS:\n%s\n\n' % self.status)
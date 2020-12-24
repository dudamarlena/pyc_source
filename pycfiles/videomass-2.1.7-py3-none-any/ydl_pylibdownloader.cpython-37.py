# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/ydl_pylibdownloader.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 7614 bytes
import wx, os
from threading import Thread
import time
from pubsub import pub
get = wx.GetApp()
OS = get.OS
LOGDIR = get.LOGdir
FFMPEG_URL = get.FFMPEG_url
pylibYdl = get.pylibYdl
if pylibYdl is None:
    import youtube_dl

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


class MyLogger(object):
    __doc__ = "\n    Intercepts youtube-dl's output by setting a logger object;\n    * Log messages to a logging.Logger instance.\n    https://github.com/ytdl-org/youtube-dl/tree/3e4cedf9e8cd3157df2457df7274d0c842421945#embedding-youtube-dl\n    "

    def debug(self, msg):
        wx.CallAfter((pub.sendMessage), 'UPDATE_YDL_FROM_IMPORT_EVT',
          output=msg,
          duration='',
          status='DEBUG')
        self.msg = msg

    def warning(self, msg):
        msg = 'WARNING: %s' % msg
        wx.CallAfter((pub.sendMessage), 'UPDATE_YDL_FROM_IMPORT_EVT',
          output=msg,
          duration='',
          status='WARNING')

    def error(self, msg):
        wx.CallAfter((pub.sendMessage), 'UPDATE_YDL_FROM_IMPORT_EVT',
          output=msg,
          duration='',
          status='ERROR')


def my_hook(d):
    """
    progress_hooks is A list of functions that get called on
    download progress. See  help(youtube_dl.YoutubeDL)
    """
    if d['status'] == 'downloading':
        percent = float(d['_percent_str'].strip().split('%')[0])
        duration = (
         'Downloading... {} of {} at {} ETA {}'.format(d['_percent_str'], d['_total_bytes_str'], d['_speed_str'], d['_eta_str']),
         percent)
        wx.CallAfter((pub.sendMessage), 'UPDATE_YDL_FROM_IMPORT_EVT',
          output='',
          duration=duration,
          status='DOWNLOAD')
    if d['status'] == 'finished':
        wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
          count='',
          duration='',
          fname='',
          end='ok')
        wx.CallAfter((pub.sendMessage), 'UPDATE_YDL_FROM_IMPORT_EVT',
          output='',
          duration='Done downloading, now converting ...',
          status='FINISHED')


class Ydl_DL_Pylib(Thread):
    __doc__ = '\n    Embed youtube-dl as module into a separated thread in order\n    to get output in real time during downloading and conversion .\n    For a list of available options see:\n\n    <https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L129-L279>\n    <https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/options.py>\n\n    or by help(youtube_dl.YoutubeDL)\n    '

    def __init__(self, varargs, logname):
        """
        Attributes defined here:
        self.stop_work_thread:  process terminate value
        self.urls:          urls list
        self.opt:           option dict data type to adding
        self.outputdir:     pathname destination
        self.count:         increases progressive account elements
        self.countmax:      length of self.urls items list
        self.logname:       file name to log messages for logging
        """
        Thread.__init__(self)
        self.stop_work_thread = False
        self.urls = varargs[1]
        self.opt = varargs[4]
        self.outputdir = varargs[3]
        self.count = 0
        self.countmax = len(varargs[1])
        self.logname = logname
        if OS == 'Windows':
            self.nocheckcertificate = True
        else:
            self.nocheckcertificate = False
        self.start()

    def run(self):
        """
        """
        for url in self.urls:
            self.count += 1
            count = 'URL %s/%s' % (self.count, self.countmax)
            wx.CallAfter((pub.sendMessage), 'COUNT_EVT',
              count=count,
              duration=100,
              fname=url,
              end='')
            if self.stop_work_thread:
                break
            ydl_opts = {'format':self.opt['format'], 
             'extractaudio':self.opt['format'], 
             'outtmpl':'{}/{}'.format(self.outputdir, self.opt['outtmpl']), 
             'writesubtitles':self.opt['writesubtitles'], 
             'addmetadata':self.opt['addmetadata'], 
             'restrictfilenames':True, 
             'ignoreerrors':True, 
             'no_warnings':False, 
             'writethumbnail':self.opt['writethumbnail'], 
             'noplaylist':self.opt['noplaylist'], 
             'no_color':True, 
             'nocheckcertificate':self.nocheckcertificate, 
             'ffmpeg_location':'{}'.format(FFMPEG_URL), 
             'postprocessors':self.opt['postprocessors'], 
             'logger':MyLogger(), 
             'progress_hooks':[
              my_hook]}
            logWrite(ydl_opts, '', self.logname)
            with youtube_dl.YoutubeDL(ydl_opts) as (ydl):
                ydl.download(['{}'.format(url)])

        wx.CallAfter(pub.sendMessage, 'END_EVT')

    def stop(self):
        """
        Sets the stop work thread to terminate the process
        """
        self.stop_work_thread = True
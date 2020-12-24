# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/ydl_pylibextractinfo.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 3445 bytes
import wx
from pubsub import pub
from threading import Thread
get = wx.GetApp()
OS = get.OS
pylibYdl = get.pylibYdl
if pylibYdl is None:
    import youtube_dl

class MyLogger(object):
    __doc__ = "\n    Intercepts youtube-dl's output by setting a logger object .\n    Log messages to a logging.Logger instance.\n    https://github.com/ytdl-org/youtube-dl/tree/3e4cedf9e8cd3157df2457df7274d0c842421945#embedding-youtube-dl\n    "

    def __init__(self):
        """
        make attribute to log messages error
        """
        self.msg_error = []

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        self.msg_error.append(msg)

    def get_message(self):
        """
        get message error from error method
        """
        if not len(self.msg_error):
            return
        return self.msg_error.pop()


class Ydl_EI_Pylib(Thread):
    __doc__ = '\n    Embed youtube-dl as module into a separated thread in order\n    to get output during process (see help(youtube_dl.YoutubeDL) ) .\n    '

    def __init__(self, url):
        """
        Attributes defined here:
        self.url  str('url')
        self.data  tupla(None, None)
        """
        Thread.__init__(self)
        self.url = url
        self.data = None
        if OS == 'Windows':
            self.nocheckcertificate = True
        else:
            self.nocheckcertificate = False
        self.start()

    def run(self):
        """
        """
        mylogger = MyLogger()
        ydl_opts = {'ignoreerrors':True,  'noplaylist':True, 
         'no_color':True, 
         'nocheckcertificate':self.nocheckcertificate, 
         'logger':mylogger}
        with youtube_dl.YoutubeDL(ydl_opts) as (ydl):
            meta = ydl.extract_info((self.url), download=False)
        error = mylogger.get_message()
        if error:
            self.data = (
             None, error)
        else:
            if meta:
                self.data = (
                 meta, None)
        wx.CallAfter((pub.sendMessage), 'RESULT_EVT',
          status='')
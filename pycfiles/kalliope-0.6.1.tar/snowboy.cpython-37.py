# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/Documents/kalliope/kalliope/trigger/snowboy/snowboy.py
# Compiled at: 2018-12-02 05:49:46
# Size of source mod 2**32: 3426 bytes
import logging, os
from threading import Thread
from kalliope import Utils
from kalliope.trigger.snowboy import snowboydecoder
from cffi import FFI as _FFI

class SnowboyModelNotFounfd(Exception):
    pass


class MissingParameterException(Exception):
    pass


logging.basicConfig()
logger = logging.getLogger('kalliope')

class Snowboy(Thread):

    def __init__(self, **kwargs):
        super(Snowboy, self).__init__()
        self._ignore_stderr()
        self.interrupted = False
        self.kill_received = False
        self.sensitivity = kwargs.get('sensitivity', 0.5)
        self.callback = kwargs.get('callback', None)
        if self.callback is None:
            raise MissingParameterException('callback function is required with snowboy')
        self.pmdl = kwargs.get('pmdl_file', None)
        if self.pmdl is None:
            raise MissingParameterException('Pmdl file is required with snowboy')
        self.pmdl_path = Utils.get_real_file_path(self.pmdl)
        if not os.path.isfile(self.pmdl_path):
            raise SnowboyModelNotFounfd('The snowboy model file %s does not exist' % self.pmdl_path)
        self.detector = snowboydecoder.HotwordDetector((self.pmdl_path), sensitivity=(self.sensitivity),
          detected_callback=(self.callback),
          interrupt_check=(self.interrupt_callback),
          sleep_time=0.03)

    def interrupt_callback(self):
        """
        This function will be passed to snowboy to stop the main thread
        :return:
        """
        return self.interrupted

    def run(self):
        """
        Start the snowboy thread and wait for a Kalliope trigger word
        :return:
        """
        self.detector.daemon = True
        self.detector.start()
        self.detector.join()

    def pause(self):
        """
        pause the Snowboy main thread
        """
        logger.debug('Pausing snowboy process')
        self.detector.paused = True

    def unpause(self):
        """
        unpause the Snowboy main thread
        """
        logger.debug('Unpausing snowboy process')
        self.detector.paused = False

    def stop(self):
        """
        Kill the snowboy process
        :return: 
        """
        logger.debug('Killing snowboy process')
        self.interrupted = True
        self.detector.terminate()

    @staticmethod
    def _ignore_stderr():
        """
        Try to forward PortAudio messages from stderr to /dev/null.
        """
        ffi = _FFI()
        ffi.cdef('\n            /* from stdio.h */\n            FILE* fopen(const char* path, const char* mode);\n            int fclose(FILE* fp);\n            FILE* stderr;  /* GNU C library */\n            FILE* __stderrp;  /* Mac OS X */\n            ')
        stdio = ffi.dlopen(None)
        devnull = stdio.fopen(os.devnull.encode(), b'w')
        try:
            stdio.stderr = devnull
        except KeyError:
            try:
                stdio._Snowboy__stderrp = devnull
            except KeyError:
                stdio.fclose(devnull)
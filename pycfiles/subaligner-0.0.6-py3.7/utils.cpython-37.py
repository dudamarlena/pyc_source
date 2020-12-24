# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/subaligner/utils.py
# Compiled at: 2020-02-25 13:05:05
# Size of source mod 2**32: 5331 bytes
import os, subprocess
from pycaption import CaptionConverter, SRTReader, DFXPWriter, DFXPReader, SRTWriter
from .exception import TerminalException

class Utils(object):
    __doc__ = 'Utility functions\n    '

    @staticmethod
    def srt2ttml(srt_file_path, ttml_file_path=None):
        """Convert SubRip subtitles to TTML subtitles.

        Arguments:
            srt_file_path {string} -- The path to the SubRip file.
            ttml_file_path {string} -- The path to the TTML file.
        """
        converter = CaptionConverter()
        with open(srt_file_path, 'r') as (file):
            converter.read(file.read(), SRTReader())
        if ttml_file_path is None:
            ttml_file_path = srt_file_path.replace('.srt', '.xml')
        with open(ttml_file_path, 'wb') as (file):
            file.write(converter.write(DFXPWriter()).encode('utf-8'))

    @staticmethod
    def ttml2srt(ttml_file_path, srt_file_path=None):
        """Convert TTML subtitles to SubRip subtitles.

        Arguments:
            ttml_file_path {string} -- The path to the TTML file.
            srt_file_path {string} -- The path to the SubRip file.
        """
        converter = CaptionConverter()
        with open(ttml_file_path, 'r') as (file):
            converter.read(file.read(), DFXPReader())
        if srt_file_path is None:
            srt_file_path = ttml_file_path.replace('.xml', '.srt')
        with open(srt_file_path, 'wb') as (file):
            file.write(converter.write(SRTWriter()).encode('utf-8'))

    @staticmethod
    def srt2vtt(srt_file_path, vtt_file_path=None, timeout_secs=30):
        """Convert SubRip subtitles to WebVTT subtitles.

        Arguments:
            srt_file_path {string} -- The path to the SubRip file.
            vtt_file_path {string} -- The path to the WebVTT file.
        """
        if vtt_file_path is None:
            vtt_file_path = srt_file_path.replace('.srt', '.vtt')
        command = 'ffmpeg -y -i {0} -f webvtt {1}'.format(srt_file_path, vtt_file_path)
        with subprocess.Popen((command.split()),
          shell=False, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE), close_fds=True) as (process):
            try:
                try:
                    _, std_err = process.communicate(timeout_secs)
                    if process.returncode != 0:
                        raise TerminalException('Cannot convert SubRip to WebVTT: {}'.format(srt_file_path))
                except subprocess.TimeoutExpired as te:
                    try:
                        process.kill()
                        process.wait()
                        raise TerminalException('Timeout on converting SubRip to WebVTT: {}'.format(srt_file_path)) from te
                    finally:
                        te = None
                        del te

                except Exception as e:
                    try:
                        process.kill()
                        process.wait()
                        if isinstance(e, TerminalException):
                            raise e
                        else:
                            raise TerminalException('Cannot convert SubRip to WebVTT: {}'.format(srt_file_path)) from e
                    finally:
                        e = None
                        del e

            finally:
                os.system('stty sane')

    @staticmethod
    def vtt2srt(vtt_file_path, srt_file_path=None, timeout_secs=30):
        """Convert WebVTT subtitles to SubRip subtitles.

        Arguments:
            vtt_file_path {string} -- The path to the WebVTT file.
            srt_file_path {string} -- The path to the SubRip file.
        """
        if srt_file_path is None:
            srt_file_path = vtt_file_path.replace('.vtt', '.srt')
        command = 'ffmpeg -y -i {0} -f srt {1}'.format(vtt_file_path, srt_file_path)
        with subprocess.Popen((command.split()),
          shell=False, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE), close_fds=True) as (process):
            try:
                try:
                    _, std_err = process.communicate(timeout_secs)
                    if process.returncode != 0:
                        raise TerminalException('Cannot convert WebVTT to SubRip: {}'.format(vtt_file_path))
                except subprocess.TimeoutExpired as te:
                    try:
                        process.kill()
                        process.wait()
                        raise TerminalException('Timeout on converting WebVTT to SubRip: {}'.format(vtt_file_path)) from te
                    finally:
                        te = None
                        del te

                except Exception as e:
                    try:
                        process.kill()
                        process.wait()
                        if isinstance(e, TerminalException):
                            raise e
                        else:
                            raise TerminalException('Cannot convert WebVTT to SubRip: {}'.format(vtt_file_path)) from e
                    finally:
                        e = None
                        del e

            finally:
                os.system('stty sane')

    @staticmethod
    def suppress_lib_logs():
        import os, logging
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '2'
        logging.getLogger('tensorflow').disabled = True
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/mime.py
# Compiled at: 2017-02-20 12:08:06
# Size of source mod 2**32: 2034 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import mimetypes, magic
from threading import Lock
__mime_lock = Lock()

def mime_type(filename):
    """ Guess mime type for the given file name

        Note: this implementation uses python_magic package which is not thread-safe, as a workaround global lock is
        used for the ability to work in threaded environment

        :param filename: file name to guess
        :return: str
        """
    try:
        __mime_lock.acquire()
        extension = filename.split('.')
        extension = extension[(len(extension) - 1)]
        if extension == 'woff2':
            return 'application/font-woff2'
        else:
            if extension == 'css':
                return 'text/css'
            m = magic.from_file(filename, mime=True)
            m = m.decode() if isinstance(m, bytes) else m
            if m == 'text/plain':
                guessed_type = mimetypes.guess_type(filename)[0]
                if guessed_type:
                    pass
                return guessed_type
            return m
    finally:
        __mime_lock.release()
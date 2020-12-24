# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aehostd/base.py
# Compiled at: 2019-11-15 11:20:52
# Size of source mod 2**32: 2115 bytes
"""
aehostd.base - very basic stuff
"""
import os, logging

def dict_del(dct, key):
    """
    removes a dictionary element given by `key' but without failing if it
    does not exist
    """
    try:
        del dct[key]
    except KeyError:
        pass


class IdempotentFile:
    __doc__ = '\n    Class handles a idempotent file on disk\n    '

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '%s.%s(%r)' % (self.__class__.__module__, self.__class__.__name__, self.path)

    def read(self):
        """
        reads content from file
        """
        try:
            with open(self.path, 'rb') as (fileobj):
                content = fileobj.read()
        except Exception as err:
            try:
                content = None
                logging.warning('Error reading file %r: %s', self.path, err)
            finally:
                err = None
                del err

        else:
            return content

    def write(self, content, remove=False, mode=None):
        """
        writes content to file if needed
        """
        exists = os.path.exists(self.path)
        if exists:
            if content == self.read():
                logging.debug('Content of %r (%d bytes) did not change => skip updating', self.path, len(content))
                return False
        if exists:
            if remove:
                try:
                    os.remove(self.path)
                except OSError:
                    pass

        try:
            with open(self.path, 'wb') as (fileobj):
                fileobj.write(content)
            if mode is not None:
                os.chmod(self.path, mode)
        except Exception as err:
            try:
                updated = False
                logging.error('Error writing content to file %r: %s', self.path, err)
            finally:
                err = None
                del err

        else:
            updated = True
            logging.info('Wrote new content (%d bytes) to file %r', len(content), self.path)
        return updated
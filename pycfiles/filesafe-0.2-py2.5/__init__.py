# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/filesafe/__init__.py
# Compiled at: 2009-04-17 20:50:08
from os import path
from re import compile
INVALID_FILE_CHARS = compile('[?%*:|"<>/]')
INVALID_DIR_CHARS = compile('[?%*:|"<>]')
filetypes = {'dir': INVALID_DIR_CHARS, 'file': INVALID_FILE_CHARS}

def get_sanitized_path(pathlist):
    """Turn a list of path elements into a path, while sanitizing the characters"""
    return path.join(*[ INVALID_FILE_CHARS.sub('_', subpath) for subpath in pathlist ])


class Chroot(object):
    """    The Chroot class gives you an easy way to protect your filestore from the
    ravages of user input.  All error handling is via raised IOError
    exceptions.  This allows you to use the same error handling mechanisms
    already in place for your file handling code.
    """

    def __init__(self, chrootpath, sanitize_method=None):
        """        Initialize a Chroot class by passing in the directory to restrict file
        operations to.  Additionally, you can pass in a sanitization method to
        decide how to handle unwanted characts.  The only currently supported
        sanitization method is None, i.e. raise an IOError exception for
        invalid filenames.

        
        """
        if sanitize_method not in (None, 'strip', 'encode'):
            sanitize_method = None
        self.sanitize_method = sanitize_method
        self.chroot = path.abspath(self.__sanitize('dir', chrootpath)) + path.sep
        if not path.isdir(self.chroot):
            raise IOError
        return

    def __sanitize(self, filetype, dirname):
        if not self.sanitize_method:
            if filetypes[filetype].search(dirname):
                raise IOError
            return dirname
        raise NotImplementedError('The only sanitization method currently supported is none')

    def __call__(self, filepath):
        filechroot = path.abspath(self.__sanitize('dir', filepath))
        if not filechroot.startswith(self.chroot):
            raise IOError
        if filechroot == self.chroot:
            raise IOError
        return filechroot
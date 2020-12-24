# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/filewriter.py
# Compiled at: 2019-11-28 13:06:28
from __future__ import absolute_import, division, print_function, unicode_literals
import os
from benchexec import util

class FileWriter(object):
    """
    The class FileWriter is a wrapper for writing content into a file.
    """

    def __init__(self, filename, content):
        """
        The constructor of FileWriter creates the file.
        If the file exist, it will be OVERWRITTEN without a message!
        """
        self.filename = filename
        self.__needsRewrite = False
        self.__content = content
        util.write_file(content, self.filename)

    def append(self, newContent, keep=True):
        """
        Add content to the represented file.
        If keep is False, the new content will be forgotten during the next call
        to this method.
        """
        content = self.__content + newContent
        if keep:
            self.__content = content
        if self.__needsRewrite:
            tmpFilename = self.filename + b'.tmp'
            util.write_file(content, tmpFilename)
            os.rename(tmpFilename, self.filename)
        else:
            with open(self.filename, b'a') as (file):
                file.write(newContent)
        self.__needsRewrite = not keep

    def replace(self, newContent):
        self.__content = b''
        self.__needsRewrite = True
        self.append(newContent)
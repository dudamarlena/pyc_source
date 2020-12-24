# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/wirecurly/dialplan/filestring.py
# Compiled at: 2014-01-08 15:34:56
import logging
from wirecurly.exc import *
from wirecurly.dialplan.expression import *
import os
log = logging.getLogger(__name__)
__all__ = [
 'FileString']

class FileString(object):
    """
                Filestring oject to use with playback app in dialplan.
        """

    def __init__(self, *argv):
        super(FileString, self).__init__()
        self.audios = []
        self.path = ''
        for i in argv:
            self.addAudio(i)

    def addAudio(self, audio):
        """
                        Add an audio file to FileString object
                """
        self.audios.append(audio)

    def setPath(self, path):
        """
                        Set Path for audios
                """
        self.path = path

    def toString(self):
        """
                        Return a string to use with playback app
                """
        return 'file_string://%s' % ('!').join([ '%s%s' % (self.path, a) for a in self.audios ])
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\batchly_sdk\request\irequest.py
# Compiled at: 2015-09-28 10:19:12
import abc

class IRequest(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, id, content_path, parameters):
        self._id = id
        self._contentPath = content_path
        self._parameters = parameters

    @property
    def id(self):
        """
            Identifier for the unit of work.

            Type: String
        """
        return self._id

    @property
    def content_path(self):
        """
            Current working directory. An isoldated work area for processing.
            Maintain temporary data and output in this folder.

            Type: String
        """
        return self._contentPath

    @property
    def parameters(self):
        """
            Key-Value configuration data for processing. You can plan for a list of paramters for your code.
            Configure them in the portal and values can be updated for each execution.

            Type: Dictionary
        """
        return self._parameters
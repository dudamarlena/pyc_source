# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/null.py
# Compiled at: 2018-05-07 08:52:27
# Size of source mod 2**32: 1707 bytes
"""
This module contains the Null plugin for fastr
"""
from fastr.core.ioplugin import IOPlugin

class Null(IOPlugin):
    __doc__ = '\n    The Null plugin is create to handle ``null://`` type or URLs. These URLs\n    are indicating the sink should not do anything. The data is not written to\n    anywhere. Besides the scheme, the rest of the URL is ignored.\n    '
    scheme = 'null'

    def __init__(self):
        super(Null, self).__init__()

    def put_url(self, inpath, outurl):
        """
        Put the files to the external data store.

        :param inpath: path of the local data
        :param outurl: url to where to store the data, starts with ``file://``
        """
        return True

    def put_value(self, value, outurl):
        """
        Put the value in the external data store.

        :param value: value to store
        :param outurl: url to where to store the data, starts with ``file://``
        """
        return True
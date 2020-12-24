# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/file_name.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 960 bytes


class FileName(object):
    __doc__ = 'The filename of an Attachment.'

    def __init__(self, file_name=None):
        """Create a FileName object

        :param file_name: The file name of the attachment
        :type file_name: string, optional
        """
        self._file_name = None
        if file_name is not None:
            self.file_name = file_name

    @property
    def file_name(self):
        """The file name of the attachment.

        :rtype: string
        """
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        """The file name of the attachment.

        :param value: The file name of the attachment.
        :type value: string
        """
        self._file_name = value

    def get(self):
        """
        Get a JSON-ready representation of this FileName.

        :returns: This FileName, ready for use in a request body.
        :rtype: string
        """
        return self.file_name
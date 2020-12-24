# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/Directory.py
# Compiled at: 2019-04-10 08:37:31
# Size of source mod 2**32: 2365 bytes
import os, fastr
from fastr.core.version import Version
from fastr.data import url
from fastr.datatypes import URLType

class Directory(URLType):
    __doc__ = '\n    DataType representing a directory.\n    '
    description = 'A directory on the disk'
    extension = None

    def _validate(self):
        """
        Validate the value of the DataType.

        :return: flag indicating validity of Boolean
        :rtype: bool
        """
        value = self.value
        if url.isurl(self.value):
            value = url.get_path_from_url(value)
        try:
            return os.path.isdir(value)
        except ValueError:
            return False

    def __eq__(self, other):
        """
        Directories are equal by default as long as the validatity matches.

        :param Directory other: other to compare against
        :return: equality flag
        """
        return self.valid == other.valid

    def action(self, name):
        """
        This method makes sure the Directory exists. A Tool can indicate an
        action that should be called for an Output which will be called before
        execution.

        :param str name: name of the action to execute
        :return: None
        """
        if name is None:
            pass
        else:
            if name == 'ensure':
                if url.isurl(self.value):
                    dir_name = url.get_path_from_url(self.value)
                else:
                    dir_name = self.value
                fastr.log.debug('ensuring {} exists.'.format(dir_name))
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
            else:
                fastr.log.warning('unknown action')
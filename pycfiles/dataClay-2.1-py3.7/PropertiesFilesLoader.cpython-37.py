# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/PropertiesFilesLoader.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 2534 bytes
""" Class description goes here. """
from abc import ABCMeta, abstractmethod
import re, six
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

@six.add_metaclass(ABCMeta)
class PropertyFile(object):
    __doc__ = 'Abstract property-holder class.\n\n    All Property Files used in dataClay must have it own class, derived from\n    this one. This function provides the basic line-by-line iteration and a\n    commonruntime interface, but the details on each line stored data is dependant\n    on each file.\n\n    WARNING: ** Not implemented **\n      - Multiline property lines\n      - Escaping sequences\n    '
    _prop_comment = re.compile('\\s*([#!].*)?$')
    _prop_regular_line = re.compile('\\s*(.*?)\\s*[=:]\\s*(.*)$')

    def __init__(self, file_name):
        """Open the file (which is expected to be a properties Java file) and read.

        This constructor relies on subclasses implementing their own
        process_line method, which will be called for each line.

        :param file_object: An object-like (stream) for the ".properties" file.
        :return:
        """
        with open(file_name, 'r') as (file_object):
            for line in file_object:
                m = self._prop_comment.match(line) or self._prop_regular_line.match(line)
                if m is not None:
                    self._process_line(m.group(1), m.group(2))

    @abstractmethod
    def _process_line(self, key, value):
        """Process a line of the ongoing properties file.

        This method should be implemented in derived classes and the internal
        class structure updated according to this properties' file needs.

        :param key: The key for the line being processed.
        :param value: The value (string) for the previous key.
        :return: None
        """
        pass


class PropertyDict(PropertyFile):
    __doc__ = 'Simple dictionary wrapper for a "properties" file.'

    def __init__(self, file_name):
        super(PropertyDict, self).__init__(file_name)

    def _process_line(self, key, value):
        """Simply store the values in the internal dictionary."""
        self.__dict__[key] = value
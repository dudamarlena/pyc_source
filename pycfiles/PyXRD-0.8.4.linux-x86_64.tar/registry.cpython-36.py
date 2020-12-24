# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/registry.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1953 bytes
from .base_group_parser import BaseGroupBarser

class ParserNamespace(object):
    __doc__ = '\n        ParserNamespace instances can be used to register parsers and bundle\n        them for easier retrieval of file filters etc.\n    '

    def __init__(self, name, group_description='All supported files'):
        self._parsers = []
        self.name = name
        self.group_description = group_description

    def register_parser(self, first=False):
        """ 
            Register a parsers to this namespace
        """

        def wrapped_register(cls):
            if first:
                self._parsers.insert(0, cls)
            else:
                self._parsers.append(cls)
            self._update_group_parser()
            return cls

        return wrapped_register

    def get_file_filters(self):
        """ 
            Returns all the file filter object for the parsers registered in 
            this namespace 
        """
        for parser in [self._group_parser] + self._parsers:
            yield parser.file_filter

    def get_export_file_filters(self):
        for parser in self._parsers:
            if parser.can_write:
                yield parser.file_filter

    def get_import_file_filters(self):
        for parser in [self._group_parser] + self._parsers:
            if parser.can_read:
                yield parser.file_filter

    def _update_group_parser(self):
        """
            Factory function for creating BaseGroupParser sub-classes,
            using the namespace's name as the class name and the list of parser
            classes as arguments.
        """
        self._group_parser = type(self.name, (BaseGroupBarser,), dict(description=(self.group_description),
          parsers=(self._parsers)))
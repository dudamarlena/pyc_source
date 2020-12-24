# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/core/scripts.py
# Compiled at: 2020-04-26 16:42:29
# Size of source mod 2**32: 2304 bytes
"""
Module that contains script data definitions for DCCs
"""
from __future__ import print_function, division, absolute_import
from tpDcc.libs.python import path, fileio
from tpDcc.core import data

class ScriptTypes(object):
    __doc__ = '\n    Class that defines different script types supported by DCCs\n    '
    Unknown = 'Unknown'
    Python = 'script.python'
    Manifest = 'script.manifest'


class ScriptExtensions(object):
    __doc__ = '\n    Class that defines different script extensions supported by DCCs\n    '
    Python = 'py'
    Manifest = 'json'


class ScriptData(data.FileData, object):
    __doc__ = '\n    Class used to define scripts stored in disk files\n    '

    def save(self, lines, comment=None):
        file_path = path.join_path(self.directory, self._get_file_name())
        write_file = fileio.FileWriter(file_path=file_path)
        write_file.write(lines, last_line_empty=False)
        version = fileio.FileVersion(file_path=file_path)
        version.save(comment=comment)

    def set_lines(self, lines):
        self.lines = lines

    def create(self):
        super(ScriptData, self).create()
        file_name = self.get_file()
        if not hasattr(self, 'lines'):
            return
        if self.lines:
            if file_name:
                write = fileio.FileWriter(file_path=file_name)
                write.write(self.lines)


class ScriptManifestData(ScriptData, object):
    __doc__ = '\n    Class used to define manifest scripts stored in disk files\n    '

    @staticmethod
    def get_data_type():
        return ScriptTypes.Manifest

    @staticmethod
    def get_data_extension():
        return ScriptExtensions.Manifest

    @staticmethod
    def get_data_title():
        return 'Scripts Manifest'


class ScriptPythonData(ScriptData, object):
    __doc__ = '\n    Class used to define Python scripts stored in disk files\n    '

    @staticmethod
    def get_data_type():
        return ScriptTypes.Python

    @staticmethod
    def get_data_extension():
        return ScriptExtensions.Python

    @staticmethod
    def get_data_title():
        return 'Python Script'

    def open(self):
        lines = ''
        return lines
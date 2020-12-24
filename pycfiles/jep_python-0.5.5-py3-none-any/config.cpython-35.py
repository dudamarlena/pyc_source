# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\jep_py\config.py
# Compiled at: 2016-01-01 10:37:49
# Size of source mod 2**32: 3611 bytes
"""JEP service configuration."""
import hashlib, re
from os.path import splitext, abspath, exists, dirname, join, basename
import datetime
BUFFER_LENGTH = 65536
TIMEOUT_SELECT_SEC = 0.5
TIMEOUT_LAST_MESSAGE = datetime.timedelta(minutes=10, seconds=30)

class ServiceConfig:
    __doc__ = 'Represents configuration of a single JEP service.'

    def __init__(self, config_file_path, patterns, command, checksum):
        self.config_file_path = abspath(config_file_path)
        self.patterns = set(patterns)
        self.command = command
        self.checksum = checksum

    @property
    def selector(self):
        """Key used during selection of the backend service to run for a certain file."""
        return hash((self.config_file_path, tuple(self.patterns)))


class ServiceConfigProvider:
    __doc__ = 'Loads JEP configuration files and provides a matching service configuration.'
    REPAT_SERVICE_SPEC = re.compile('^(?P<patterns>[^:]+)\\s*:\\s*^(?P<command>.*)$\\s*', re.MULTILINE)
    REPAT_FILE_PATTERN = re.compile('[^,\\s]+')

    @classmethod
    def provide_for(cls, edited_file_name, config_file_name='.jep'):
        """Returns service configuration for given file name that is going to be edited."""
        lastdir = None
        curdir = dirname(abspath(edited_file_name))
        extension_pattern = cls._file_pattern(edited_file_name)
        filename = basename(edited_file_name)
        search_patterns = {extension_pattern, filename}
        while curdir != lastdir:
            config_file_path = join(curdir, config_file_name)
            if exists(config_file_path):
                for config in cls._configurations(config_file_path):
                    if not search_patterns.isdisjoint(config.patterns):
                        return config

            lastdir = curdir
            curdir = dirname(curdir)

    @classmethod
    def _file_pattern(cls, file_name):
        """Determine file pattern to look for in config file, either *.ext or basename."""
        base, ext = splitext(file_name)
        if ext:
            return '*%s' % ext
        else:
            return basename(file_name)

    @classmethod
    def _configurations(cls, config_file_path):
        """Iterator over service configurations in config file."""
        with open(config_file_path) as (config_file):
            content = config_file.read()
            checksum = cls._checksum(content)
        for m in cls.REPAT_SERVICE_SPEC.finditer(content):
            patterns = cls.REPAT_FILE_PATTERN.findall(m.group('patterns'))
            if patterns:
                yield ServiceConfig(config_file_path, patterns, m.group('command'), checksum)

    @classmethod
    def checksum(cls, config_file_path):
        """Computes a checksum over content of given file."""
        try:
            with open(config_file_path) as (config_file):
                content = config_file.read()
            return cls._checksum(content)
        except FileNotFoundError:
            return

    @classmethod
    def _checksum(cls, string):
        """Computes a checksum over given string."""
        return hashlib.sha1(string.encode()).digest()
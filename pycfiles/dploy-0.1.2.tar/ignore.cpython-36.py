# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/arecarn/Dropbox/projects/dploy/master/dploy/ignore.py
# Compiled at: 2017-10-27 00:13:39
# Size of source mod 2**32: 1911 bytes
"""
Module for the --ignore IGNORE_PATTERN flag and .dploystowignore file
"""
import pathlib
from dploy import utils

class Ignore:
    __doc__ = '\n    Handles ignoring of files via glob patterns either passed in directly in or\n    in a specified ignore file.\n    '

    def __init__(self, patterns, source):
        if patterns is None:
            input_patterns = []
        else:
            input_patterns = patterns
        self.ignored_files = []
        file = source.parent / pathlib.Path('.dploystowignore')
        self.patterns = [
         str(file.name)]
        self.patterns.extend(input_patterns)
        self._read_ignore_file_patterns(file)

    def _read_ignore_file_patterns(self, file):
        """
        read ignore patterns from a specified file
        """
        try:
            with open(str(file)) as (afile):
                file_patterns = afile.read().splitlines()
                self.patterns.extend(file_patterns)
        except FileNotFoundError:
            pass

    def should_ignore(self, source):
        """
        check if a source should be ignored, based on the ignore patterns in
        self.patterns

        This checks if the ignore patterns match either the file exactly or
        its parents
        """
        for pattern in self.patterns:
            try:
                files = sorted(source.parent.glob(pattern))
            except IndexError:
                continue

            for file in files:
                if utils.is_same_file(file, source) or source in file.parents:
                    return True

        return False

    def ignore(self, file):
        """
        add a file to be ignored
        """
        self.ignored_files.append(file)

    def get_ignored_files(self):
        """
        get a list of the files that have been ignored
        """
        return self.ignored_files
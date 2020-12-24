# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chaos/globber.py
# Compiled at: 2015-02-17 11:45:34
__doc__ = ' Helper functions for file and directory globbing. '
from __future__ import absolute_import
import os, fnmatch

class Globber(object):
    """
        Traverses a directory and returns all absolute filenames.
        """

    def __init__(self, path, include=None, recursive=True):
        """
                Initialize Globber parameters. Filter may be a list of globbing patterns.

                Parameters
                ----------
                path: string
                        Absolute path to the directory to glob
                include: list of strings
                        List of globbing pattern strings. By default, ALL files in the given path
                        are globbed.
                recursive: boolean
                        When True: will traverse subdirectories found in $path. Defaults to True.
                """
        if include is None:
            include = [
             '*']
        self.path = path
        self.include = include
        self.recursive = recursive
        return

    def glob(self):
        """
                Traverse directory, and return all absolute filenames of files that
                match the globbing patterns.
                """
        matches = []
        for root, dirnames, filenames in os.walk(self.path):
            if not self.recursive:
                while len(dirnames) > 0:
                    dirnames.pop()

            for include in self.include:
                for filename in fnmatch.filter(filenames, include):
                    matches.append(os.path.join(root, filename))

        return matches
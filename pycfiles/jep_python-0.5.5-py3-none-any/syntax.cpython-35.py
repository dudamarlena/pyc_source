# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\jep_py\syntax.py
# Compiled at: 2015-12-07 10:17:47
# Size of source mod 2**32: 2678 bytes
"""Management of code and DSL syntax definitions."""
import collections

class SyntaxFile:
    __doc__ = 'Container for reference to syntax file and the extensions it supports.'

    def __init__(self, name, path, fileformat, extensions):
        self.name = name
        self.path = path
        self.fileformat = fileformat
        self.extensions = [self.normalized_extension(e) for e in extensions]
        self._definition = None

    def __eq__(self, other):
        return self.name == other.name and self.path == other.path and self.fileformat == other.fileformat and self.extensions == other.extensions

    def __hash__(self):
        return hash(self.path)

    @classmethod
    def normalized_extension(cls, extension):
        """Returns extension in normalized form, i.e. without leading dot and all lower capitals."""
        if not extension:
            return
        else:
            if extension.startswith('.'):
                return extension[1:].lower()
            return extension.lower()

    @property
    def definition(self):
        if not self._definition:
            with open(self.path) as (syntaxfile):
                self._definition = syntaxfile.read()
        return self._definition


class SyntaxFileSet(collections.MutableSet):
    __doc__ = 'Collection of SyntaxFiles, with additional lookup of syntax by extension.'

    def __init__(self):
        self.data = set()
        self.extension_map = dict()

    def __contains__(self, x):
        return x in self.data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def add(self, value):
        self.data.add(value)
        for extension in value.extensions:
            self.extension_map[extension] = value

    def add_syntax_file(self, name, path, fileformat, extensions):
        self.add(SyntaxFile(name, path, fileformat, extensions))

    def discard(self, value):
        if value in self.data:
            self.data.discard(value)
            for extension in value.extensions:
                self.extension_map.pop(extension)

    def filtered(self, fileformat, extensions):
        """Returns a filtered (Python) set for the given extensions and in the specified file file format."""
        if extensions:
            syntax_files = {self.extension_map[ext] for ext in extensions if ext in self.extension_map}
        else:
            syntax_files = self.data
        return set(filter(lambda s: s.fileformat is fileformat, syntax_files))
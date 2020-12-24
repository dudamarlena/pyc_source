# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flap\substitutions\files.py
# Compiled at: 2016-09-29 04:18:11
# Size of source mod 2**32: 3734 bytes
from re import compile, split, DOTALL
from itertools import chain
from flap.engine import Fragment
from flap.substitutions.commons import Substitution

class FileSubstitution(Substitution):
    __doc__ = '\n    Replace the link to a TeX file by its content\n    '

    def replacements_for(self, fragment, match):
        included_file = self.flap.find_tex_source(fragment, match.group(1), self.tex_file_extensions())
        return self.flap.raw_fragments_from(included_file)

    @staticmethod
    def tex_file_extensions():
        return ['tex']


class Input(FileSubstitution):
    __doc__ = "\n    Detects fragments that contains an input directive (such as '\\input{foo}).\n    When one is detected, it extracts all the fragments from the file that\n    is referred (such as 'foo.tex')\n    "

    def __init__(self, delegate, flap):
        super().__init__(delegate, flap)

    def prepare_pattern(self):
        return compile('\\\\input\\s*\\{([^}]+)\\}')


class SubFile(FileSubstitution):
    __doc__ = "\n    Detects fragments that contains an subfile directive (i.e., '\\subfile{foo}').\n    When one is detected, it extracts all the fragments from the file that\n    is referred (such as 'foo.tex')\n    "

    def __init__(self, delegate, flap):
        super().__init__(delegate, flap)

    def prepare_pattern(self):
        return compile('\\\\subfile\\s*\\{([^}]+)\\}')


class SubFileExtractor(Substitution):
    __doc__ = "\n    Extract the content of the 'subfile', that is the text between\n    \x08egin{document} and \\end{document}.\n    "

    def __init__(self, delegate, flap):
        super().__init__(delegate, flap)

    def prepare_pattern(self):
        return compile('\\\\documentclass(?:\\[[^\\]]+\\])?\\{subfiles\\}.*\\\\begin\\{document\\}(.+)\\\\end\\{document\\}', DOTALL)

    def replacements_for(self, fragment, match):
        if match is None:
            raise ValueError('This is not a valid subfile!')
        return [
         fragment.extract(match, 1)]


class IncludeOnly(Substitution):
    __doc__ = "\n    Detects '\\includeonly' directives and notify the engine to later\n    discard the specified files.\n    "

    def prepare_pattern(self):
        return compile('\\\\includeonly\\{([^\\}]+)\\}')

    def replacements_for(self, fragment, match):
        included_files = split(',', match.group(1))
        self.flap.restrict_inclusion_to(included_files)
        return []


class Include(Input):
    __doc__ = '\n    Matches `\\include{file.tex}`. It replaces them by the content of the\n    file and append a \\clearpage after.\n    '

    def __init__(self, delegate, flap):
        super().__init__(delegate, flap)

    def prepare_pattern(self):
        return compile('\\\\include\\s*\\{([^}]+)\\}')

    def replacements_for(self, fragment, match):
        if self.flap.is_ignored(match.group(1)):
            return []
        else:
            return chain(super().replacements_for(fragment, match), [
             Fragment(fragment.file(), fragment.line_number(), '\\clearpage ')])
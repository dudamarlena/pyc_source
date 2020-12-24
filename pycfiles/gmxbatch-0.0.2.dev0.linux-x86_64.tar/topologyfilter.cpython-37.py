# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/topfilter/topologyfilter.py
# Compiled at: 2020-03-09 07:07:33
# Size of source mod 2**32: 6109 bytes
import warnings
from typing import Tuple, List, Optional, Sequence, Dict

class ParseError(Exception):
    __doc__ = 'Error raised when a parsing error occurs.'


class TopologyFilter:
    __doc__ = 'Simple preprocessor for GROMACS topology files\n    '
    filename: str
    defines: Dict[(str, List[str])]
    ifdefs: List[Tuple[(str, bool)]]
    section = None
    section: Optional[str]
    handleincludes = True
    handleincludes: bool
    handleifdefs = True
    handleifdefs: bool
    handleempty = True
    handleempty: bool

    def __init__(self, filename: str, defines: Optional[Sequence[str]]=None, handleincludes: bool=True, handleifdefs: bool=True, handleempty: bool=True):
        """Initialize the preprocessor

        :param filename: main file name
        :type filename: str
        :param defines: set of defined macros
        :type defines: set of str
        :param handleincludes: if True, follow #include directives. If False, pass them through
        :type handleincludes: bool
        :param handleifdefs: if True, handle preprocessor conditionals. If False, pass them throgh
        :type handleifdefs: bool
        :param handleempty: if True, hide empty (or pure comment) lines. If False, pass them through
        :type handleempty: bool
        """
        self.handleempty = handleempty
        self.handleincludes = handleincludes
        self.handleifdefs = handleifdefs
        self.defines = dict(zip(defines, [[]] * len(defines))) if defines else {}
        self.filename = filename
        self.ifdefs = []

    def parse(self, filename: Optional[str]=None):
        """Start parsing the file.

        This is a generator. Yields the following:
            - stripped line (str),
            - comment (str or None),
            - current section name (str or None),
            - file name (str),
            - line number (int),
            - full line (str)

        Empty lines, are not yielded.

        #ifdef/#ifndef/#else/#endif lines are only yielded if `self.handleifdefs` is set to False.

        #include lines are only yielded if `self.handleincludes` is set to False.

        :param filename: the file name to parse. Do not set this by yourself, leave it None
        :type filename: str or None
        """
        if filename is None:
            filename = self.filename
            self.ifdefs = []
            self.section = None
        with open(filename, 'rt') as (f):
            for i, line in enumerate(f, start=1):
                try:
                    l, *comment = line.split(';', 1)
                    comment = None if not comment else comment[0]
                    l = l.strip()
                    if l.startswith('#ifdef') and self.handleifdefs:
                        _, macro = l.split()
                        self.ifdefs.append((macro, True))
                    else:
                        if l.startswith('#ifndef') and self.handleifdefs:
                            _, macro = l.split()
                            self.ifdefs.append((macro, False))
                        else:
                            if l.startswith('#else') and self.handleifdefs:
                                self.ifdefs[-1] = (
                                 self.ifdefs[(-1)][0], not self.ifdefs[(-1)][1])
                            else:
                                if l.startswith('#endif') and self.handleifdefs:
                                    del self.ifdefs[-1]
                                else:
                                    if l.startswith('#include'):
                                        if self.handleincludes:
                                            _, incfilename = l.split()
                                            if incfilename.startswith('"'):
                                                if not (incfilename.endswith('"') or incfilename.startswith('<') and incfilename.endswith('>')):
                                                    raise ParseError(f"Invalid #include directive in file {f.name} at line #{i}.")
                                                self.parse(incfilename)
                                            else:
                                                pass
                    if self.ifdefs_allow_reading() or self.handleifdefs or l.startswith('#define'):
                        _, macro, *values = l.split()
                        self.defines[macro] = values
                    else:
                        if l.startswith('#undef'):
                            _, macro = l.split()
                            del self.defines[macro]
                        else:
                            if l.startswith('#error'):
                                _, message = l.split(None, 1)
                                raise ParseError(f"#error directive encountered with message: {message}")
                            else:
                                if l.startswith('#warn'):
                                    directive, message = l.split(None, 1)
                                    warnings.warn(f"{directive} directive encountered with message: {message}")
                                else:
                                    if l.startswith('[') and l.endswith(']'):
                                        self.section = l[1:-1].strip()
                                        yield (l, comment, self.section, f.name, i, line)
                                    else:
                                        if (l or self).handleempty:
                                            pass
                                        else:
                                            yield (
                                             l, comment, self.section, f.name, i, line)
                except (ValueError, IndexError):
                    raise ParseError(f"Error in file {filename} on line #{i}: {line}")

    def defined(self, macro: str) -> bool:
        """Check if a preprocessor macro is #defined or not"""
        return macro in self.defines

    def ifdefs_allow_reading(self) -> bool:
        """Check if the current state of #ifdef and #ifndef clauses allow reading/interpreting or not."""
        return all([self.defined(macro) and state or not self.defined(macro) and not state for macro, state in self.ifdefs])
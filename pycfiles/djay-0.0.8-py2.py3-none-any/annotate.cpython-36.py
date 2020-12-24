# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/coverage/coverage/annotate.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 3097 bytes
"""Source file annotation for Coverage."""
import os, re
from coverage.backward import sorted
from coverage.report import Reporter

class AnnotateReporter(Reporter):
    __doc__ = "Generate annotated source files showing line coverage.\n\n    This reporter creates annotated copies of the measured source files. Each\n    .py file is copied as a .py,cover file, with a left-hand margin annotating\n    each line::\n\n        > def h(x):\n        -     if 0:   #pragma: no cover\n        -         pass\n        >     if x == 1:\n        !         a = 1\n        >     else:\n        >         a = 2\n\n        > h(2)\n\n    Executed lines use '>', lines not executed use '!', lines excluded from\n    consideration use '-'.\n\n    "

    def __init__(self, coverage, config):
        super(AnnotateReporter, self).__init__(coverage, config)
        self.directory = None

    blank_re = re.compile('\\s*(#|$)')
    else_re = re.compile('\\s*else\\s*:\\s*(#|$)')

    def report(self, morfs, directory=None):
        """Run the report.

        See `coverage.report()` for arguments.

        """
        self.report_files(self.annotate_file, morfs, directory)

    def annotate_file(self, cu, analysis):
        """Annotate a single file.

        `cu` is the CodeUnit for the file to annotate.

        """
        if not cu.relative:
            return
        else:
            filename = cu.filename
            source = cu.source_file()
            if self.directory:
                dest_file = os.path.join(self.directory, cu.flat_rootname())
                dest_file += '.py,cover'
            else:
                dest_file = filename + ',cover'
        dest = open(dest_file, 'w')
        statements = sorted(analysis.statements)
        missing = sorted(analysis.missing)
        excluded = sorted(analysis.excluded)
        lineno = 0
        i = 0
        j = 0
        covered = True
        while True:
            line = source.readline()
            if line == '':
                break
            lineno += 1
            while i < len(statements) and statements[i] < lineno:
                i += 1

            while j < len(missing) and missing[j] < lineno:
                j += 1

            if i < len(statements) and statements[i] == lineno:
                covered = j >= len(missing) or missing[j] > lineno
            if self.blank_re.match(line):
                dest.write('  ')
            else:
                if self.else_re.match(line):
                    if i >= len(statements):
                        if j >= len(missing):
                            dest.write('! ')
                    else:
                        if i >= len(statements) or j >= len(missing):
                            dest.write('> ')
                        else:
                            if statements[i] == missing[j]:
                                dest.write('! ')
                            else:
                                dest.write('> ')
                else:
                    if lineno in excluded:
                        dest.write('- ')
                    else:
                        if covered:
                            dest.write('> ')
                        else:
                            dest.write('! ')
            dest.write(line)

        source.close()
        dest.close()
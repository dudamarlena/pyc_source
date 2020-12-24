# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/coverage/coverage/summary.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 2972 bytes
"""Summary reporting"""
import sys
from coverage.report import Reporter
from coverage.results import Numbers
from coverage.misc import NotPython

class SummaryReporter(Reporter):
    __doc__ = 'A reporter for writing the summary report.'

    def __init__(self, coverage, config):
        super(SummaryReporter, self).__init__(coverage, config)
        self.branches = coverage.data.has_arcs()

    def report(self, morfs, outfile=None):
        """Writes a report summarizing coverage statistics per module.

        `outfile` is a file object to write the summary to.

        """
        self.find_code_units(morfs)
        max_name = max([len(cu.name) for cu in self.code_units] + [5])
        fmt_name = '%%- %ds  ' % max_name
        fmt_err = '%s   %s: %s\n'
        header = fmt_name % 'Name' + ' Stmts   Miss'
        fmt_coverage = fmt_name + '%6d %6d'
        if self.branches:
            header += ' Branch BrMiss'
            fmt_coverage += ' %6d %6d'
        width100 = Numbers.pc_str_width()
        header += '%*s' % (width100 + 4, 'Cover')
        fmt_coverage += '%%%ds%%%%' % (width100 + 3,)
        if self.config.show_missing:
            header += '   Missing'
            fmt_coverage += '   %s'
        rule = '-' * len(header) + '\n'
        header += '\n'
        fmt_coverage += '\n'
        if not outfile:
            outfile = sys.stdout
        outfile.write(header)
        outfile.write(rule)
        total = Numbers()
        for cu in self.code_units:
            try:
                analysis = self.coverage._analyze(cu)
                nums = analysis.numbers
                args = (cu.name, nums.n_statements, nums.n_missing)
                if self.branches:
                    args += (nums.n_branches, nums.n_missing_branches)
                args += (nums.pc_covered_str,)
                if self.config.show_missing:
                    args += (analysis.missing_formatted(),)
                outfile.write(fmt_coverage % args)
                total += nums
            except KeyboardInterrupt:
                raise
            except:
                report_it = not self.config.ignore_errors
                if report_it:
                    typ, msg = sys.exc_info()[:2]
                    if typ is NotPython:
                        if not cu.should_be_python():
                            report_it = False
                if report_it:
                    outfile.write(fmt_err % (cu.name, typ.__name__, msg))

        if total.n_files > 1:
            outfile.write(rule)
            args = ('TOTAL', total.n_statements, total.n_missing)
            if self.branches:
                args += (total.n_branches, total.n_missing_branches)
            args += (total.pc_covered_str,)
            if self.config.show_missing:
                args += ('', )
            outfile.write(fmt_coverage % args)
        return total.pc_covered
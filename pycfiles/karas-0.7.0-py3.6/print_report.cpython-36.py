# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/extensions/print_report.py
# Compiled at: 2019-01-08 08:44:30
# Size of source mod 2**32: 3192 bytes
import os, sys
from karas.training import extension
from karas.training import utils
from karas.training.extensions import log_report as log_report_module

class PrintReport(extension.Extension):
    __doc__ = 'Trainer extension to print the accumulated results.\n\n    This extension uses the log accumulated by a :class:`LogReport` extension\n    to print specified entries of the log in a human-readable format.\n\n    Args:\n        entries (list of str): List of keys of observations to print.\n        log_report (str or LogReport): Log report to accumulate the\n            observations. This is either the name of a LogReport extensions\n            registered to the trainer, or a LogReport instance to use\n            internally.\n        out: Stream to print the bar. Standard output is used by default.\n\n    '

    def __init__(self, entries, log_report='LogReport', out=sys.stdout):
        self._entries = entries
        self._log_report = log_report
        self._out = out
        self._log_len = 0
        entry_widths = [max(10, len(s)) for s in entries]
        header = ('  '.join('{:%d}' % w for w in entry_widths).format)(*entries) + '\n'
        self._header = header
        self._show_header = True
        templates = []
        for entry, w in zip(entries, entry_widths):
            templates.append((entry, '{:<%dg}  ' % w, ' ' * (w + 2)))

        self._templates = templates

    def __call__(self, trainer):
        out = self._out
        if self._show_header:
            out.write(self._header)
            self._show_header = False
        else:
            log_report = self._log_report
            if isinstance(log_report, str):
                log_report = trainer.get_extension(log_report)
            else:
                if isinstance(log_report, log_report_module.LogReport):
                    log_report(trainer)
                else:
                    raise TypeError('log report has a wrong type %s' % type(log_report))
        log = log_report.log
        log_len = self._log_len
        while len(log) > log_len:
            if os.name == 'nt':
                utils.erase_console(0, 0)
            else:
                out.write('\x1b[1A')
                out.write('\x1b[J')
            self._print(log[log_len])
            log_len += 1

        self._log_len = log_len
        if os.name != 'nt':
            out.write(self._header)

    def _print(self, observation):
        out = self._out
        for entry, template, empty in self._templates:
            if entry in observation:
                out.write(template.format(observation[entry]))
            else:
                out.write(empty)

        out.write('\n')
        if hasattr(out, 'flush'):
            out.flush()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_out']
        state['_log_len'] = 0
        state['_show_header'] = True
        return state

    def __setstate__(self, state):
        state['_out'] = sys.stdout
        self.__dict__.update(state)
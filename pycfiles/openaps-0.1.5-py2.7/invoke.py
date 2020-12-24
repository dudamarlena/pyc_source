# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/reports/invoke.py
# Compiled at: 2016-04-27 23:44:05
"""
invoke   - generate a report
"""
from __future__ import print_function
from openaps.reports.report import Report
from openaps import uses
import reporters, sys, argparse

def configure_app(app, parser):
    """
  """
    parser._actions[(-1)].nargs = '+'


def main(args, app):
    requested = args.report[:]
    for spec in requested:
        report = app.actions.selected(args).reports[spec]
        device = app.devices[report.fields['device']]
        task = app.actions.commands['add'].usages.commands[device.name].method.commands[report.fields['use']]
        app.parser.set_defaults(**task.method.from_ini(report.fields))
        args, extra = app.parser.parse_known_args(app.inputs)
        print(report.format_url())
        repo = app.git_repo()
        try:
            output = task.method(args, app)
        except Exception as e:
            print(report.name, ' raised ', e, file=sys.stderr)
            app.epilog()
            raise
        else:
            reporters.Reporter(report, device, task)(output)
            print('reporting', report.name)
            repo.git.add([report.name], write_extension_data=False)
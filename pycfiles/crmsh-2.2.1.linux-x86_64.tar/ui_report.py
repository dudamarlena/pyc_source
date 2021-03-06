# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/ui_report.py
# Compiled at: 2016-05-04 07:56:27
import os, subprocess
from signal import signal, SIGPIPE, SIG_DFL
from . import utils
from . import config
from . import options

def report_tool():
    toolopts = [
     os.path.join(config.path.sharedir, 'hb_report', 'hb_report'),
     'hb_report',
     'crm_report']
    for tool in toolopts:
        if utils.is_program(tool):
            return tool

    return


def create_report(context, args):
    extcmd = report_tool()
    if not extcmd:
        context.fatal_error('No reporting tool found')
    extraopts = str(config.core.report_tool_options).strip().split()
    cmd = [extcmd] + extraopts + list(args)
    if options.regression_tests:
        print '.EXT', cmd
    return subprocess.call(cmd, shell=False, preexec_fn=lambda : signal(SIGPIPE, SIG_DFL))
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/ctznosx/usage.py
# Compiled at: 2014-08-23 00:33:36
from __future__ import unicode_literals

def _(text):
    return text.strip(b'\n')


HELP = _(b'\n  -h, --help         show help message\n  -v, --version      show version\n  --verbose          show script while running\n  --dry-run          show script without running\n\ncommands:\n  run                invoke the scanner\n  device             manage device\n  monitor            manage monitors\n  report             display report\n\n')
USAGE = _(b'\n                                  MMP"""""YMM MP""""""`MM M""MMMM""M\n           dP                     M\' .mmm. `M M  mmmmm..M M  `MM\'  M\n           88                     M  MMMMM  M M.      `YM MM.    .MM\n.d8888b. d8888P d888888b 88d888b. M  MMMMM  M MMMMMMM.  M M  .mm.  M\n88\'  `""   88      .d8P\' 88\'  `88 M. `MMM\' .M M. .MMM\'  M M  MMMM  M\n88.  ...   88    .Y8P    88    88 MMb     dMM Mb.     .dM M  MMMM  M\n`88888P\'   dP   d888888P dP    dP MMMMMMMMMMM MMMMMMMMMMM MMMMMMMMMM\n\nUsage: ctznosx [--config=CONFIG] command\n\n%s' % HELP)
MONITOR_USAGE = _(b'\nUsage: ctznosx monitor [ install | list | upgrade | remove ]\n\ncommands:\n  list               show all installed monitors\n  install            installs specified monitor\n  upgrade            upgrades specified monitor\n  remove             removes specified monitor\n')
MANAGER_USAGE = _(b'\nUsage: ctznosx manager [ register ]\n\ncommands:\n  register           register this device with a remote server\n')
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/commands/reporters.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1485 bytes
from dexy.commands.utils import print_indented
from dexy.commands.utils import print_rewrapped
import dexy.reporter

def reporters_command(alias=False, simple=False):
    """
    List available reports which dexy can run.
    """
    if simple:
        for reporter in dexy.reporter.Reporter:
            print(reporter.alias)

    else:
        if alias:
            nodoc_settings = ('aliases', 'help')
            reporter = dexy.reporter.Reporter.create_instance(alias)
            print_indented('%s Reporter' % reporter.__class__.__name__)
            print('')
            print_indented('settings:')
            print('')
            for name in sorted(reporter._instance_settings):
                if name in nodoc_settings:
                    continue
                docs, default_value = reporter._instance_settings[name]
                print_indented(name, 2)
                print_rewrapped(docs, 4)
                print_indented('(default: %r)' % default_value, 4)
                print('')

            reporter.help()
            print('')
        else:
            FMT = '%-15s %-9s %s'
            print(FMT % ('alias', 'default', 'info'))
            for reporter in dexy.reporter.Reporter:
                help_text = reporter.setting('help').splitlines()[0]
                default_text = reporter.setting('default') and 'true' or 'false'
                print(FMT % (reporter.alias, default_text, help_text))
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/droopescan/dscan/droopescan.py
# Compiled at: 2019-06-14 01:34:00
# Size of source mod 2**32: 1659 bytes
from __future__ import print_function
from cement.core import backend, foundation, controller, handler
from cement.utils.misc import init_defaults
from dscan.common.functions import template, version_get
from dscan import common
from dscan.plugins import Scan
import dscan, os, signal, sys

def handle_interrupt(signal, stack):
    print('\nShutting down...')
    common.shutdown = True


signal.signal(signal.SIGINT, handle_interrupt)

class DroopeScanBase(controller.CementBaseController):

    class Meta:
        label = 'base'
        description = '\n    |\n ___| ___  ___  ___  ___  ___  ___  ___  ___  ___\n|   )|   )|   )|   )|   )|___)|___ |    |   )|   )\n|__/ |    |__/ |__/ |__/ |__   __/ |__  |__/||  /\n                    |\n=================================================\n'
        epilog = template('help_epilog.mustache')

    @controller.expose(hide=True)
    def default(self):
        print(template('intro.mustache', {'version': version_get(), 
         'color': True}))


class DroopeScan(foundation.CementApp):
    testing = False

    class Meta:
        label = 'droopescan'
        base_controller = DroopeScanBase
        exit_on_close = False


def main():
    ds = DroopeScan('DroopeScan', plugin_config_dir=dscan.PWD + './plugins.d', plugin_dir=dscan.PWD + './plugins', catch_signals=None)
    handler.register(Scan)
    try:
        try:
            ds.setup()
            ds.run()
        except RuntimeError as e:
            if not ds.debug and not ds.testing:
                print(e, file=sys.stdout)
            else:
                raise

    finally:
        ds.close()
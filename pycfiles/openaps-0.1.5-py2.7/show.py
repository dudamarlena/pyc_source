# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/vendors/plugins/show.py
# Compiled at: 2016-02-06 13:50:19
"""
Show/list vendor plugins

"""
from openaps.cli import helpers
from vendor import Vendor

def configure_app(app, parser):
    parser.set_defaults(name='*')
    parser._actions[(-1)].nargs = '?'
    parser._actions[(-1)].choices.append('*')
    helpers.install_show_arguments(parser)


def main(args, app):
    for plugin in Vendor.FromConfig(app.config):
        if args.name in ['*', plugin.name]:
            print args.format(plugin)
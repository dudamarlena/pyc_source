# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/vendors/plugins/add.py
# Compiled at: 2015-12-15 13:09:24
"""
Add a new vendor plugin to openaps-environment.
"""
from vendor import Vendor

def configure_app(app, parser):
    parser._actions[(-1)].choices = None
    parser.add_argument('--path', default='.', help="Path to module's namespace")
    return


def main(args, app):
    vendor = Vendor(args.name, path=args.path)
    try:
        module = vendor.get_module()
        vendor.add_option('module', module.__name__)
        vendor.store(app.config)
        app.config.save()
        print 'added', vendor.format_url()
    except ImportError as e:
        print e
        print ("{name:s} doesn't seem to be an importable python module\nIf it is a python module, try using --path to influence\nPYTHONPATH\n      ").format(name=args.name)
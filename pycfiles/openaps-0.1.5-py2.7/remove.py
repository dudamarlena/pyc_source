# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/vendors/plugins/remove.py
# Compiled at: 2015-12-15 13:09:24
"""
Remove vendor plugin from openaps-environment
"""
from vendor import Vendor

def main(args, app):
    for plugin in Vendor.FromConfig(app.config):
        if args.name == plugin.name:
            plugin.remove(app.config)
            app.config.save()
            print 'removed', plugin.format_url()
            break
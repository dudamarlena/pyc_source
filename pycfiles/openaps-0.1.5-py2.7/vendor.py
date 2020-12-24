# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/vendors/plugins/vendor.py
# Compiled at: 2016-02-07 00:43:35
import importlib, site
from openaps.configurable import Configurable

class Vendor(Configurable):
    prefix = 'vendor'
    required = ['name']
    optional = []
    fields = {}
    url_template = '{name:s}://'
    name = None

    def __init__(self, name=None, **kwds):
        self.name = name
        self.fields = dict(**kwds)

    def get_module(self):
        site.addsitedir(self.fields.get('path'))
        return importlib.import_module(self.name)
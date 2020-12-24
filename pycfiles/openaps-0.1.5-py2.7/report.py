# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/reports/report.py
# Compiled at: 2016-02-06 13:50:19
import json
from openaps.configurable import Configurable

class Report(Configurable):
    prefix = 'report'
    required = ['report', 'reporter', 'device', 'use']
    optional = []
    fields = {}
    url_template = '{device:s}://{reporter:s}/{use:s}/{name:s}'
    name = None

    def __init__(self, name=None, report=None, reporter=None, device=None, use=None, **kwds):
        self.name = report or name
        self.fields = dict(reporter=reporter, device=device, use=use, **kwds)
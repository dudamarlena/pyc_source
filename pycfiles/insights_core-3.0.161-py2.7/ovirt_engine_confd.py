# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ovirt_engine_confd.py
# Compiled at: 2019-05-16 13:41:33
from .. import Parser, parser, LegacyItemAccess
from insights.specs import Specs

@parser(Specs.ovirt_engine_confd)
class OvirtEngineConfd(LegacyItemAccess, Parser):

    def parse_content(self, content):
        self.data = dict((k.strip('" '), v.strip('" ')) for k, _, v in [ l.partition('=') for l in content ])
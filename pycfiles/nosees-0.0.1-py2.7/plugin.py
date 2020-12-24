# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/nosees/plugin.py
# Compiled at: 2018-07-12 08:51:53
import logging, os
from nose.plugins import Plugin
from mock import patch
from nosees.mock import mock_es
log = logging.getLogger('nose.plugins.nosees')

class FakeElasticsearchPlugin(Plugin):
    name = 'noes-es'

    def options(self, parser, env=os.environ):
        super(FakeElasticsearchPlugin, self).options(parser, env=env)

    def configure(self, options, conf):
        super(FakeElasticsearchPlugin, self).configure(options, conf)
        if not self.enabled:
            return

    def begin(self):
        if self.enabled:
            mock_es()
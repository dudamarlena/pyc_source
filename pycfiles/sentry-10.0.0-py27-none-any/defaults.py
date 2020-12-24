# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/projectoptions/defaults.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.projectoptions import register
LATEST_EPOCH = 2
DEFAULT_GROUPING_CONFIG = 'legacy:2019-03-12'
register(key='sentry:grouping_config', epoch_defaults={1: DEFAULT_GROUPING_CONFIG})
DEFAULT_GROUPING_ENHANCEMENTS_BASE = 'legacy:2019-03-12'
register(key='sentry:grouping_enhancements_base', epoch_defaults={1: DEFAULT_GROUPING_ENHANCEMENTS_BASE})
register(key='sentry:grouping_enhancements', default='')
register(key='sentry:fingerprinting_rules', default='')
register(key='sentry:default_loader_version', epoch_defaults={1: '4.x', 2: '5.x'})
register(key='sentry:builtin_symbol_sources', epoch_defaults={1: ['ios'], 2: ['ios', 'microsoft']})
register(key='filters:legacy-browsers', epoch_defaults={1: '0'})
register(key='filters:web-crawlers', epoch_defaults={1: '1'})
register(key='filters:browser-extensions', epoch_defaults={1: '0'})
register(key='filters:localhost', epoch_defaults={1: '0'})
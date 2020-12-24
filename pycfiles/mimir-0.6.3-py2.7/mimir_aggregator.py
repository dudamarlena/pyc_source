# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted/plugins/mimir_aggregator.py
# Compiled at: 2012-05-10 08:39:36
try:
    from twisted.application.service import ServiceMaker
except ImportError:
    from twisted.scripts.mktap import _tapHelper as ServiceMaker

mimirAggregator = ServiceMaker('Mimir Aggregator', 'mimir.aggregator.tap', 'Mimir Feed Aggregator and Feeder', 'aggregator')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/rhv_log_collector_analyzer.py
# Compiled at: 2019-05-16 13:41:33
"""
RHV Log Collector Analyzer
==========================

RHV Log Collector Analyzer is a tool that analyze RHV sosreports
and live systems.

This module provides processing for the output of
rhv-log-collector-analyzer --json which will be running
in a live system to detect possible issues.
"""
from .. import JSONParser, parser, CommandParser
from insights.specs import Specs

@parser(Specs.rhv_log_collector_analyzer)
class RhvLogCollectorJson(CommandParser, JSONParser):
    """
    Class to parse the output of ``rhv-log-collector-analyzer --json``.
    """
    pass
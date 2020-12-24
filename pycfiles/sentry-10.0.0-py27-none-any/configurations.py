# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/grouping/strategies/configurations.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.grouping.strategies.base import create_strategy_configuration
CLASSES = []
CONFIGURATIONS = {}

def register_strategy_config(id, **kwargs):
    rv = create_strategy_configuration(id, **kwargs)
    if rv.config_class not in CLASSES:
        CLASSES.append(rv.config_class)
    CONFIGURATIONS[rv.id] = rv
    return rv


register_strategy_config(id='legacy:2019-03-12', strategies=[
 'expect-ct:v1',
 'expect-staple:v1',
 'hpkp:v1',
 'csp:v1',
 'threads:legacy',
 'stacktrace:legacy',
 'chained-exception:legacy',
 'template:v1',
 'message:v1'], delegates=[
 'frame:legacy', 'stacktrace:legacy', 'single-exception:legacy'], changelog='\n        * Traditional grouping algorithm\n        * Some known weaknesses with regards to grouping of native frames\n    ')
register_strategy_config(id='newstyle:2019-04-05', strategies=[
 'expect-ct:v1',
 'expect-staple:v1',
 'hpkp:v1',
 'csp:v1',
 'threads:v1',
 'stacktrace:v1',
 'chained-exception:v1',
 'template:v1',
 'message:v1'], delegates=[
 'frame:v1', 'stacktrace:v1', 'single-exception:v1'], changelog='\n        * New grouping strategy optimized for native and javascript\n        * Not compatible with the old legacy grouping\n    ')
register_strategy_config(id='newstyle:2019-04-17', strategies=[
 'expect-ct:v1',
 'expect-staple:v1',
 'hpkp:v1',
 'csp:v1',
 'threads:v1',
 'stacktrace:v1',
 'chained-exception:v1',
 'template:v1',
 'message:v2'], delegates=[
 'frame:v2', 'stacktrace:v1', 'single-exception:v2'], changelog='\n        * messages are now preprocessed to increase change of grouping together\n        * exceptions without stacktraces are now grouped by a trimmed message\n    ')
register_strategy_config(id='newstyle:2019-05-08', strategies=[
 'expect-ct:v1',
 'expect-staple:v1',
 'hpkp:v1',
 'csp:v1',
 'threads:v1',
 'stacktrace:v1',
 'chained-exception:v1',
 'template:v1',
 'message:v2'], delegates=[
 'frame:v3', 'stacktrace:v1', 'single-exception:v2'], changelog='\n        * context lines are honored again for platforms with reliable source\n          code information (JavaScript, Python, PHP and Ruby)\n        * JavaScript stacktraces are better deduplicated across browser\n          versions.\n        * JavaScript stacktraces involving source maps are likely to group\n          better.\n    ')
register_strategy_config(id='combined:2019-04-07', strategies=[
 'expect-ct:v1',
 'expect-staple:v1',
 'hpkp:v1',
 'csp:v1',
 'threads:v1',
 'stacktrace:v1nl',
 'chained-exception:v1nl',
 'template:v1',
 'message:v1'], delegates=[
 'frame:v1nl', 'stacktrace:v1nl', 'single-exception:v1nl'], changelog='\n        * Uses `newstyle:2019-04-05` for native platforms\n        * Uses `legacy:2019-03-12` for all other platforms\n    ')
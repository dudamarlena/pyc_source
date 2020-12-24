# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/plugins/never_fires.py
# Compiled at: 2019-05-16 13:41:33
from insights import combiner, rule, make_pass
CONTENT = 'This should never display'

@combiner()
def thing():
    raise Exception


@rule(thing)
def report(t):
    return make_pass('THING')
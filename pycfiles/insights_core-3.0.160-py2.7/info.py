# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/plugins/info.py
# Compiled at: 2019-11-14 13:57:46
from insights import rule, make_fail, make_pass, make_info

@rule()
def report():
    return make_fail('SOME_FAIL', foo='bar')


@rule()
def report2():
    return make_pass('SOME_PASS', foo='bar')


@rule()
def report3():
    return make_info('SOME_INFO', foo='bar')
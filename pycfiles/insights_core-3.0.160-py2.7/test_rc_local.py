# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rc_local.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.rc_local import RcLocal
from insights.tests import context_wrap
RC_LOCAL_DATA = ("\n#!/bin/sh\n#\n# This script will be executed *after* all the other init scripts.\n# You can put your own initialization stuff in here if you don't\n# want to do the full Sys V style init stuff.\n\ntouch /var/lock/subsys/local\necho never > /sys/kernel/mm/redhat_transparent_hugepage/enabled\n").strip()

def test_rc_local():
    rc_local = RcLocal(context_wrap(RC_LOCAL_DATA))
    assert len(rc_local.data) == 2
    assert rc_local.data[0] == 'touch /var/lock/subsys/local'
    assert rc_local.get('kernel') == ['echo never > /sys/kernel/mm/redhat_transparent_hugepage/enabled']
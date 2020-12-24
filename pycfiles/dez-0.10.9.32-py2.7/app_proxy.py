# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/app_proxy.py
# Compiled at: 2015-11-19 18:49:54
from dez.http.application import HTTPApplication

def main(**kwargs):
    a = HTTPApplication('', kwargs['port'])
    a.add_proxy_rule('/', kwargs['domain'], 80)
    a.add_static_rule('/static/', '.')
    a.start()
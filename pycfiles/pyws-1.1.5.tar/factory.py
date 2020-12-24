# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/factory.py
# Compiled at: 2013-08-11 10:36:51
import os, suds
wsdl_path = os.path.abspath(os.path.dirname(__file__)) + '/test.wsdl'

def build_client():
    return suds.client.Client('file://%s' % wsdl_path, cache=None)
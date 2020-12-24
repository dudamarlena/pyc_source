# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/helper/get_local_ip.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'get_local_ip']
__authors__ = ['Tim Chow']
import netifaces

def get_local_ip(exclude_interfaces=None):
    if exclude_interfaces is None:
        exclude_interfaces = []
    else:
        if isinstance(exclude_interfaces, str):
            exclude_interfaces = [
             exclude_interfaces]
        elif not isinstance(exclude_interfaces, (list, tuple)):
            raise TypeError('expect None, str, list or tuple, not %s' % type(exclude_interfaces).__name__)
        for interface in netifaces.interfaces():
            if interface in exclude_interfaces:
                continue
            for address in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                yield address['addr']

    return
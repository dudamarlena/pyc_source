# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/hook/signals.py
# Compiled at: 2014-12-31 04:01:41
import django.dispatch

def InstanceSignal(providing_args=[]):
    """Return a Signal instance that will always send an instance argument,
    and provided args
    """
    args = [
     'instance'] + providing_args
    return django.dispatch.Signal(providing_args=args)
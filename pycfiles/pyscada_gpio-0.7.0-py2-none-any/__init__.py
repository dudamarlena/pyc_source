# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/martin/Documents/PyScada/python/PyScada-GPIO/pyscada/gpio/__init__.py
# Compiled at: 2019-12-16 11:20:30
from __future__ import unicode_literals
import pyscada
__version__ = b'0.7.0'
__author__ = b'Martin Schröder'
default_app_config = b'pyscada.gpio.apps.PyScadaGPIOConfig'
PROTOCOL_ID = 10
parent_process_list = [
 {b'pk': PROTOCOL_ID, b'label': b'pyscada.gpio', 
    b'process_class': b'pyscada.gpio.worker.Process', 
    b'process_class_kwargs': b'{"dt_set":30}', 
    b'enabled': True}]
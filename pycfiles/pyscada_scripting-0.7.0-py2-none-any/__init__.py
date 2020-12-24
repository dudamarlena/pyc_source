# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
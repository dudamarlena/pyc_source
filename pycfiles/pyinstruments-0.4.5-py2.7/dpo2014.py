# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\visa\dpo2014.py
# Compiled at: 2013-11-18 09:03:09
"""module to interface the DPO3014 scope (using VISA interface)"""
from pyhardware.drivers.visa.dpo3014 import DPO3014

class DPO2014(DPO3014):
    _supported_models = [
     'DPO2014']
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\visa\dpo2014.py
# Compiled at: 2013-11-18 09:03:09
__doc__ = 'module to interface the DPO3014 scope (using VISA interface)'
from pyhardware.drivers.visa.dpo3014 import DPO3014

class DPO2014(DPO3014):
    _supported_models = [
     'DPO2014']
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/test/hydro/topology/conf.py
# Compiled at: 2014-11-23 10:45:29
__author__ = 'yanivshalev'
from hydro import Configurator
from hydro.base_classes import HydroStr, HydroDatetime, HydroList
conf = Configurator.config_builder()
conf.OPTIMIZER = 'TestTopology'
conf.PLAN_ALLOWED_PARAMETERS = {'CLIENT_ID': {'type': HydroStr}, 'FROM_DATE': {'type': HydroDatetime}, 'TO_DATE': {'type': HydroDatetime}, 'EVENT_TYPES': {'type': HydroList}}
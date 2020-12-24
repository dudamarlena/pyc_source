# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/toonapilib/toonapilib/configuration.py
# Compiled at: 2019-10-20 07:41:04
# Size of source mod 2**32: 1640 bytes
"""A place to store the configuration."""
STATE_CACHING_SECONDS = 300
THERMOSTAT_STATE_CACHING_SECONDS = 3600
STATES = {0:'Comfort', 
 1:'Home', 
 2:'Sleep', 
 3:'Away', 
 4:'Holiday', 
 5:'Unknown'}
BURNER_STATES = {0:'off', 
 1:'on', 
 2:'water_heating', 
 3:'pre_heating'}
PROGRAM_STATES = {0:'off', 
 1:'on', 
 2:'manual'}
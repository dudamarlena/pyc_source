# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\jonat\code\snek_cogs\tarot\cogs\tarot\t_data\json_data.py
# Compiled at: 2020-01-06 10:13:36
# Size of source mod 2**32: 373 bytes
import json, os
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
with open(DIR_PATH + '/tarot_spreads.json') as (f):
    tarot_spreads = json.load(f)
with open(DIR_PATH + '/tarot_data.json') as (f):
    tarot_data = json.load(f)
with open(DIR_PATH + '/tarot_skins.json') as (f):
    tarot_skins = json.load(f)
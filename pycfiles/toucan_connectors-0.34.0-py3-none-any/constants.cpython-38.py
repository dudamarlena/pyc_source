# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/aircall/constants.py
# Compiled at: 2020-04-21 05:29:37
# Size of source mod 2**32: 453 bytes
"""File containing constants for AirCall connector"""
COLUMN_DICTIONARY = {'calls':[
  'id',
  'direction',
  'duration',
  'answered_at',
  'ended_at',
  'raw_digits',
  'user_id',
  'tags',
  'user_name',
  'team',
  'day'], 
 'tags':[
  'id', 'name', 'color', 'description'], 
 'users':[
  'team', 'user_id', 'user_name', 'user_created_at']}
MAX_RUNS = 1
PER_PAGE = 50
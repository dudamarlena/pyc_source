# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/datawatcher/status.py
# Compiled at: 2020-01-10 04:27:31
# Size of source mod 2**32: 2973 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '31/05/2017'
OBSERVATION_STATUS = {'not processing':0, 
 'parsing':1, 
 'none found':2, 
 'starting':3, 
 'started':4, 
 'waiting for acquisition ending':5, 
 'acquisition ended':6, 
 'acquisition canceled':7, 
 'failure':-1, 
 'aborted':-2}
DICT_OBS_STATUS = {}
for name, value in OBSERVATION_STATUS.items():
    DICT_OBS_STATUS[value] = name

DET_END_XML = '[scan].xml'
PARSE_INFO_FILE = '[scan].info'
DET_END_USER_ENTRY = 'from file pattern'
DET_END_METHODS = (
 DET_END_XML, PARSE_INFO_FILE, DET_END_USER_ENTRY)
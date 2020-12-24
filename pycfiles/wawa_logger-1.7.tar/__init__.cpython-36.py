# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chud/projects/wawa_logger/wawa_logger/__init__.py
# Compiled at: 2019-09-10 11:17:26
# Size of source mod 2**32: 836 bytes
from requests import post
url = 'http://wpg1psint001.linux.wmic.ins:8001/log/pub'

def publish(**kwargs):
    """
    sends data based on input to centralized source

    params
    :tool_name
    :event_type
    :source_host
    :dest_host
    :username
    returns
    :bool True|False
    """
    noval = 'no_data'
    payload = {'tool_name':kwargs.get('tool_name'), 
     'event_type':kwargs.get('event_type'), 
     'source_host':kwargs.get('source_host', noval), 
     'dest_host':kwargs.get('dest_host', noval), 
     'username':kwargs.get('username', noval)}
    try:
        r = post(url, json=payload)
        if r.ok:
            return True
        else:
            return False
    except Exception as e:
        print(f"Exception: {e}")
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/status/status_lib/history_snapshot.py
# Compiled at: 2016-08-01 11:57:45
import logging, os
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
DOORPI_SECTION = 'DoorPi'

def get(*args, **kwargs):
    files = dict()
    try:
        if len(kwargs['name']) == 0:
            kwargs['name'] = ['']
        if len(kwargs['value']) == 0:
            kwargs['value'] = ['']
        path = kwargs['DoorPiObject'].config.get_string_parsed(DOORPI_SECTION, 'snapshot_path')
        if os.path.exists(path):
            files = [ os.path.join(path, i) for i in os.listdir(path) ]
            files = sorted(files, key=os.path.getmtime)
            if path.find('DoorPiWeb'):
                changedpath = path[path.find('DoorPiWeb') + len('DoorPiWeb'):]
                files = [ f.replace(path, changedpath) for f in files ]
        return files
    except Exception as exp:
        logger.exception(exp)
        return {'Error': 'could not create ' + str(__name__) + ' object - ' + str(exp)}
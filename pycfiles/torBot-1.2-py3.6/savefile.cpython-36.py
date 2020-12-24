# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modules/savefile.py
# Compiled at: 2018-07-01 06:51:02
# Size of source mod 2**32: 635 bytes
import json, time

def saveJson(datatype, data):
    """
        Creates json file and stores json

        Args:
            datatype: the type of the object being passed
            data = data that is being stored with object
    """
    timestr = time.strftime('%Y%m%d-%H%M%S')
    file_name = 'TorBot-Export-' + datatype + timestr + '.json'
    with open(file_name, 'w+') as (f):
        output = {datatype: data}
        json.dump(output, f, indent=2)
    print('\nData will be saved with a File Name :', file_name)
    return file_name
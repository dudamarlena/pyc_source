# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/status/status_lib/config.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)

def get(*args, **kwargs):
    try:
        if len(kwargs['name']) == 0:
            kwargs['name'] = ['']
        if len(kwargs['value']) == 0:
            kwargs['value'] = ['']
        return_dict = {}
        for section_request in kwargs['name']:
            for section in kwargs['DoorPiObject'].config.get_sections(section_request):
                return_dict[section] = {}
                for value_request in kwargs['value']:
                    for key in kwargs['DoorPiObject'].config.get_keys(section, value_request):
                        return_dict[section][key] = kwargs['DoorPiObject'].config.get(section, key)

        for section in return_dict.keys():
            if len(return_dict[section]) == 0:
                del return_dict[section]

        return return_dict
    except Exception as exp:
        logger.exception(exp)
        return {'Error': 'could not create ' + str(__name__) + ' object - ' + str(exp)}


def is_active(doorpi_object):
    if doorpi_object.config:
        return True
    return False
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/action/SingleActions/statusfile.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
from doorpi.action.base import SingleAction
import doorpi
from doorpi.status.status_class import DoorPiStatus

def write_statusfile(filename, filecontent):
    try:
        filename = doorpi.DoorPi().parse_string(filename)
        filecontent = doorpi.DoorPi().parse_string(filecontent)
        try:
            doorpi_status = DoorPiStatus(doorpi.DoorPi())
            doorpi_status_json_beautified = doorpi_status.json_beautified
            doorpi_status_json = doorpi_status.json
            filecontent = filecontent.replace('!DOORPI_STATUS.json_beautified!', doorpi_status_json_beautified)
            filecontent = filecontent.replace('!DOORPI_STATUS.json!', doorpi_status_json)
        except:
            logger.exception('error while creating status')

    except:
        logger.warning('while action statusfile - error to get DoorPi().parse_string')
        return False

    try:
        file = open(filename, 'w')
        try:
            file.write(filecontent)
            file.flush()
        finally:
            file.close()

    except IOError as e:
        logger.warning('while action statusfile - I/O error(%s): %s' % (e.errno, e.strerror))
        return False

    return True


def get(parameters):
    parameter_list = parameters.split(',')
    if len(parameter_list) < 2:
        return None
    else:
        filename = parameter_list[0]
        filecontent = ('').join(parameter_list[1:])
        return SleepAction(write_statusfile, filename, filecontent)


class SleepAction(SingleAction):
    pass
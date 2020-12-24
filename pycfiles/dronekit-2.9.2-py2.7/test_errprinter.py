# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_errprinter.py
# Compiled at: 2019-03-14 01:22:55
import logging, time
from nose.tools import assert_true
from dronekit import connect
from dronekit.test import with_sitl

@with_sitl
def test_115(connpath):
    """Provide a custom status_printer function to the Vehicle and check that
    the autopilot messages are correctly logged.
    """
    logging_check = {'ok': False}

    def errprinter_fn(msg):
        if isinstance(msg, str) and 'APM:Copter' in msg:
            logging_check['ok'] = True

    vehicle = connect(connpath, wait_ready=False, status_printer=errprinter_fn)
    i = 5
    while not logging_check['ok'] and i > 0:
        time.sleep(1)
        i -= 1

    assert_true(logging_check['ok'])
    vehicle.close()
    autopilotLogger = logging.getLogger('autopilot')
    autopilotLogger.removeHandler(autopilotLogger.handlers[0])
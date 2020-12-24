# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/inspectors/bmc.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 567 bytes
import logging
from mercury_agent.hardware.drivers import get_subsystem_drivers
from mercury_agent.inspector.inspectors import expose_late
log = logging.getLogger(__name__)

@expose_late('bmc')
def bmc_inspector(device_info):
    drivers = get_subsystem_drivers('bmc')
    if not drivers:
        return
    else:
        if len(drivers) > 1:
            log.warning('Found more than one driver for BMC. This is most likely a bug')
        driver = drivers[0]
        log.info('Running BMC inspector: {}'.format(driver.name))
        return driver.inspect()
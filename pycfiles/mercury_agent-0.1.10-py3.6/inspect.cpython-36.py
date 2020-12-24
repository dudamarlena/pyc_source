# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/inspect.py
# Compiled at: 2019-02-11 13:08:11
# Size of source mod 2**32: 2561 bytes
import logging
from mercury_agent.inspector.inspectors import inspectors, late_inspectors
from mercury_agent.hardware.drivers import registered_drivers, set_driver_cache
from mercury.common.mercury_id import generate_mercury_id
from mercury.common.exceptions import fancy_traceback_short, parse_exception
log = logging.getLogger(__name__)
global_device_info = {}

def _collect():
    _c = dict()
    for inspector, f in inspectors:
        _c[inspector] = f()

    return _c


def inspect():
    """
    Runs inspectors and associates collection with a mercury_id
    :return:
    """
    global global_device_info
    collected = _collect()
    dmi = collected.get('dmi') or {}
    interfaces = collected.get('interfaces') or {}
    collected['mercury_id'] = generate_mercury_id(dmi, interfaces)
    for driver in registered_drivers:
        _wants = driver['class'].wants
        try:
            devices = driver['class'].probe(_wants and collected[_wants] or collected)
        except Exception:
            log.error(fancy_traceback_short((parse_exception()),
              preamble=('Probe function failed for driver {}'.format(driver['name']))))
            continue

        if devices:
            set_driver_cache(driver, devices)

    for inspector, f in late_inspectors:
        collected[inspector] = f(collected)

    (global_device_info.update)(**collected)
    return global_device_info


if __name__ == '__main__':
    from pprint import pprint
    pprint(inspect())
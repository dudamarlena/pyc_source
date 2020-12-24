# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/inspectors/dmi.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 904 bytes
from . import inspector
from mercury_agent.inspector.hwlib.sysfs import DMI

@inspector.expose('dmi')
def dmi_inspector():
    dmi = DMI()
    return dmi.dump()


if __name__ == '__main__':
    import pprint
    pprint.pprint(dmi_inspector())
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/inspectors/os_storage.py
# Compiled at: 2019-04-01 22:20:26
# Size of source mod 2**32: 2511 bytes
import logging, re
from press.helpers import parted
from mercury_agent.inspector.inspectors import inspector
from mercury_agent.inspector.hwlib.udev import UDevHelper
log = logging.getLogger(__name__)

def get_disk_type(dev):
    dev = dev.lstrip('/dev/')
    sysfs_rotational_path = f"/sys/block/{dev}/queue/rotational"
    try:
        if int(open(sysfs_rotational_path).read()):
            return 'disk'
        return 'ssd'
    except (IOError, OSError):
        log.warning('Could not parse sysfs for %s', dev)
        return 'unknown'


def _fix_udev_device_for_mongo(udev_device):
    rgx = re.compile('[{}]'.format('$. '))
    for k in udev_device:
        if rgx.search(k):
            udev_device[rgx.sub('_', k)] = udev_device.pop(k)


@inspector.expose('os_storage')
def os_storage_inspector():
    os_storage = []
    storage_devices = UDevHelper().discover_valid_storage_devices(fc_enabled=True,
      loop_enabled=False)
    for storage_device in storage_devices:
        device_info = {}
        udev_device = dict(list(storage_device.items()))
        try:
            (device_info.update)(**(parted.PartedInterface(udev_device['DEVNAME'])).device_info)
        except parted.PartedException:
            log.warning('Could not parse disk label for %s. Got root?', udev_device['DEVNAME'])

        device_info['udev'] = udev_device
        if udev_device.get('ID_BUS') != 'fc':
            device_info['media_type'] = get_disk_type(udev_device['DEVNAME'])
        else:
            device_info['media_type'] = 'external'
        os_storage.append(device_info)
        _fix_udev_device_for_mongo(udev_device)

    return os_storage


if __name__ == '__main__':
    import json
    print(json.dumps((os_storage_inspector()), indent=2))
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/hwlib/lspci.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 6718 bytes
"""Provides functionality for parsing output from `lspci`."""
import shlex, six, subprocess
ETHERNET_CONTROLLER = '0200'
NETWORK_CONTROLLER = '0280'
FIBRE_CHANNEL = '0c04'
RAID_CONTROLLER = '0104'

class LSPCIError(Exception):
    __doc__ = 'Raised when something goes wrong related to the `lspci` command.'


def lspci_run(arguments='-mm'):
    """Runs lspci and returns the output.

    :param arguments: Arguments you want to pass to lspci default = '-mm'
    :return: stdout from lspci command
    :except: LSPCIException on non-zero return code
    """
    cmd = shlex.split('lspci ' + arguments)
    sub_proc = subprocess.Popen(cmd, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
    out, err = sub_proc.communicate()
    if sub_proc.returncode:
        raise LSPCIError('[%d] %s' % (sub_proc.returncode, err))
    if isinstance(out, six.binary_type):
        out = out.decode('utf-8')
    return out


def _get_lspci_id(line):
    """Read a hex ID of the form [nnnn] from an `lspci` line.

    Gets an id from a line that looks like this:
        Intel Corporation [8086]
    where 8086 is the id
    It should also work if something like this happens:
    2nd Generation Core Processor Family DRAM [not_and_id] Controller [0104]

    :param line: A string representing a line of lspci output.
    :return: A string representing the ID.
    """
    hush = line.split('[')
    return hush[(-1)].strip(']')


def _get_lspci_name(line):
    """Reads and returns a 'name' from a line of `lspci` output."""
    hush = line.split('[')
    return '['.join(hush[0:-1]).strip()


def parse_nnvmmk():
    """
    Runs lspci -nnvmmk and parses the output into a list of dictionaries.
    :return: a list of dicts with the following keys
    slot
    vendor_name
    device_name
    svendor_name
    sdevice_name
    vendor_id
    device_id
    svendor_id
    sdevice_id
    revision
    progif
    driver
    :except:
    """
    out = lspci_run('-nnvmmk')
    pcibus = list()
    blocks = out.split('\n\n')
    for block in blocks:
        device = dict()
        for element in block.splitlines():
            split_element = element.split(':')
            key = split_element[0]
            data = ':'.join(split_element[1:]).strip()
            if key in ('Slot', 'ProgIf', 'Driver'):
                device[key.lower()] = data
                continue
            if key in ('Class', 'Vendor', 'Device', 'SVendor', 'SDevice'):
                key_prefix = key.lower()
                device[key_prefix + '_name'] = _get_lspci_name(data)
                device[key_prefix + '_id'] = _get_lspci_id(data)
            else:
                if key == 'Rev':
                    device['revision'] = data
                    continue

        if not device:
            pass
        else:
            pcibus.append(device)

    return pcibus


class PCIDevice(dict):
    __doc__ = 'Represents information about a PCI Device as returned by `lspci`.'

    def __init__(self, slot=None, class_id=None, vendor_id=None, device_id=None, class_name='', vendor_name='', device_name='', svendor_name=None, svendor_id=None, sdevice_name=None, sdevice_id=None, revision=None, progif=None, driver=None):
        """Create a PCIDevice. Checks for a few required fields."""
        if None in [slot, class_id, vendor_id, device_id]:
            raise LSPCIError('slot, class_id, vendor_id, and device_id are required.')
        super(PCIDevice, self).__init__()
        self.slot = slot
        self.class_id = class_id
        self.vendor_id = vendor_id
        self.device_id = device_id
        self.class_name = class_name
        self.vendor_name = vendor_name
        self.device_name = device_name
        self.svendor_name = svendor_name
        self.svendor_id = svendor_id
        self.sdevice_name = sdevice_name
        self.sdevice_id = sdevice_id
        self.revision = revision
        self.progif = progif
        self.driver = driver

    def __getattr__(self, key):
        try:
            return self[key]
        except (KeyError, AttributeError):
            return

    def __setattr__(self, key, value):
        self[key] = value


class PCIBus(list):

    def __init__(self, sudo=False):
        super(PCIBus, self).__init__()
        for it in parse_nnvmmk():
            self.append(PCIDevice(**it))

    def get_devices_by_class(self, class_id):
        sub_li = list()
        for device in self:
            if device.get('class_id') == class_id:
                sub_li.append(device)

        return sub_li

    def has_device_class(self, class_id):
        for device in self:
            if device.get('class_id') == class_id:
                return True

        return False

    def get_devices_by_vendor(self, vendor_id):
        sub_li = list()
        for device in self:
            if device.get('vendor_id') == vendor_id:
                sub_li.append(device)

        return sub_li

    def get_fibre_channel_devices(self):
        return self.get_devices_by_class(FIBRE_CHANNEL)

    def has_fibre_channel(self):
        return self.has_device_class(FIBRE_CHANNEL)

    def get_ethernet_devices(self):
        return self.get_devices_by_class(ETHERNET_CONTROLLER)

    def has_ethernet(self):
        return self.has_device_class(ETHERNET_CONTROLLER)

    def get_network_devices(self):
        return self.get_devices_by_class(NETWORK_CONTROLLER)

    def has_network(self):
        return self.has_device_class(NETWORK_CONTROLLER)

    def get_raid_bus_controller_devices(self):
        return self.get_devices_by_class(RAID_CONTROLLER)

    def has_raid_bus_controller(self):
        return self.has_device_class(RAID_CONTROLLER)
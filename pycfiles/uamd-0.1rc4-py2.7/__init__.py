# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/uamd/__init__.py
# Compiled at: 2011-11-22 04:04:45
from IPy import IP
import cidr, device, warnings

def detect(meta, loader=cidr.default_loader):
    """
    
    Detect device via HTTP Headers and return :class:`cidr.Loader` instance.
    When ``loader`` is not None, spoof check is executed via ``loader``

    :param meta:    the HTTP Headers dict
    :param loader:  :class:`cidr.Loader` for loading CIDR via carrier for spoof check.
                    set it ``None`` to skip spoof check.
    :return:        detected device information as :class:`uamd.device.Device` subclass instance
    :type meta:     dict
    :type loader:   :class:`cidr.Loader` instance
    :rtype:         :class:`cidr.device.Device` subclass instance
    """
    dev = device.DummyDevice()
    for cls in device.devices:
        if cls.fastcheck(meta):
            dev = cls.factory(meta)
            break

    if loader and dev.carrier is not None:
        dev = spoof_check(dev, meta, loader)
    return dev


def spoof_check(device, meta, loader=cidr.default_loader):
    """
    
    Check whether the device is spoofed via reported carrier's CIDR.
    If the device accessed from out of range, then the device may be spoofed
    so the method will set ``dev.spoof = True`` and return the device.

    :param device:  the device for checking whether spoofed
    :param meta:    the HTTP Headers dict
    :param loader:  :class:`cidr.Loader` for loading CIDR via carrier for spoof check.
                    set it ``None`` to skip spoof check.
    :return:        modified(or not modified) device
    :type meta:     dict
    :type loader:   :class:`cidr.Loader` instance
    :rtype:         :class:`cidr.device.Device` subclass instance
    """
    if not loader:
        raise AttributeError('``loader`` is required to get CIDR for carrier')
    cidr = loader.get(device.carrier)
    REMOTE_ADDR = meta.get('REMOTE_ADDR', None)
    if not REMOTE_ADDR:
        warnings.warn('REMOTE_ADDR is not available. could not determine spoof.')
    else:
        device.spoof = IP(REMOTE_ADDR) not in cidr
    return device
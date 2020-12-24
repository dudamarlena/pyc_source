# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aioble/__init__.py
# Compiled at: 2019-02-01 18:18:49
# Size of source mod 2**32: 782 bytes
import platform
if platform.system() == 'Linux':
    from aioble.bluezdbus.centralmanager import CentralManagerBlueZDbus as CentralManager
    from aioble.bluezdbus.device import DeviceBlueZDbus as Device
else:
    if platform.system() == 'Darwin':
        from aioble.corebluetooth.centralmanager import CoreBluetoothCentralManager as CentralManager
        from aioble.corebluetooth.device import CoreBluetoothDevice as Device
    else:
        if platform.system() == 'Windows':
            from aioble.dotnet.centralmanager import CentralManagerDotNet as CentralManager
            from aioble.dotnet.device import DeviceDotNet as Device
        else:
            from aioble.centralmanager import CentralManager
            from aioble.device import Device
            from aioble.service import Service
            from aioble.characteristic import Characteristic
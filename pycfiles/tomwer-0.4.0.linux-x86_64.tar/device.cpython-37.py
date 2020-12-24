# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/utils/device.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 3328 bytes
"""Utils for devices (GPU, CPU...)"""
__authors__ = [
 'H. Payno']
try:
    import pycuda.driver as cuda
except ImportError:
    cuda = None

from silx.opencl import ocl

class _DeviceBase:
    __doc__ = 'base class for device definition'

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class OpenCLDevice(_DeviceBase):
    __doc__ = 'Definition of an opencl device'

    def __init__(self, name, platform_id, device_id):
        super(OpenCLDevice, self).__init__(name=name)
        self._platform_id = platform_id
        self._device_id = device_id

    @property
    def platform_id(self):
        return self._platform_id

    @property
    def device_id(self):
        return self._device_id


class CudaDevice(_DeviceBase):
    __doc__ = 'Definition of an opencl device'

    def __init__(self, name, id_):
        super(CudaDevice, self).__init__(name=name)
        self._id = id_

    @property
    def id(self):
        """

        :return: ID of the cuda device
        :rtype: int
        """
        return self._id


class _CudaPlatformBase:

    def getExistingDevices(self):
        """

        :return: all existing cuda device
        """
        devices = []
        if cuda is not None:
            cuda.init()
            for i_device in range(cuda.Device.count()):
                device = CudaDevice((cuda.Device(i_device).name()), id_=i_device)
                devices.append(device)

        return devices


class _OpenCLPlatformBase:

    def getExistingDevices(self):
        """

        :return: all existing opencl platform
        """
        devices = []
        if ocl is not None:
            for platform_id, platform in enumerate(ocl.platforms):
                for device_id, dev in enumerate(platform.devices):
                    devices.append(OpenCLDevice(name=(dev.name), platform_id=platform_id,
                      device_id=device_id))

        return devices
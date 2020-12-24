# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_device_monitor/widgets/device.py
# Compiled at: 2020-04-09 04:47:29
# Size of source mod 2**32: 1585 bytes
from fpga_i2c_bridge.appliance import I2CAppliance, I2CGenericBinary, I2CDimmer, I2CRGBDimmer, I2CShutter
from fpga_device_monitor.widgets.dimmer_ctrl import DimmerControlWidget
from fpga_device_monitor.widgets.rgb_ctrl import RGBControlWidget
from fpga_device_monitor.widgets.shutter_ctrl import ShutterControlWidget
from fpga_device_monitor.widgets.switch_ctrl import SwitchControlWidget
from fpga_device_monitor.windows.base import BaseWidget

class DeviceWidget(BaseWidget):
    __doc__ = 'Widget representing a single FPGA output device.'

    def __init__(self, device, *args, **kwargs):
        (super(DeviceWidget, self).__init__)('device.ui', *args, **kwargs)
        self.device = device
        self.control_widget = None
        self.init_ui()

    def init_ui(self) -> None:
        """Factory method that initializes the control widget, based on the type of device it was instantiated with."""
        self.group.setTitle(str(self.device))
        if isinstance(self.device, I2CGenericBinary):
            widget_class = SwitchControlWidget
        else:
            if isinstance(self.device, I2CDimmer):
                widget_class = DimmerControlWidget
            else:
                if isinstance(self.device, I2CRGBDimmer):
                    widget_class = RGBControlWidget
                else:
                    if isinstance(self.device, I2CShutter):
                        widget_class = ShutterControlWidget
                    else:
                        raise Exception('Unknown device: %s' % str(self.device))
        self.control_widget = widget_class(parent=self)
        self.group.layout().addWidget(self.control_widget)
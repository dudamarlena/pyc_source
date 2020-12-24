# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_device_monitor/__main__.py
# Compiled at: 2020-04-09 06:29:13
# Size of source mod 2**32: 942 bytes
"""Main executable of the FPGA Device Monitor."""
import argparse, sys
from qtpy import QtWidgets
from fpga_i2c_bridge import I2CBridge
from fpga_device_monitor.windows.main import MainWindow
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--bus', default='1', help='Number of I2C bus to use (default: 1)')
    argparser.add_argument('--addr', default='3E', help='I2C address of the connected FPGA (default: 3E)')
    argparser.add_argument('--dummy', action='store_true', help='Run with simulated devices only')
    args = vars(argparser.parse_args())
    i2c_bridge = I2CBridge(i2c_dummy=(args['dummy']), i2c_addr=int((args['addr']), base=16),
      i2c_bus=(int(args['bus'])))
    if args['dummy']:
        pass
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(i2c_bridge)
    window.show()
    sys.exit(app.exec_())
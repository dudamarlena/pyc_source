# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\__init__.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 3395 bytes
import os, sys, inspect
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '//')
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '//calibration')
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '//disk_test')
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '//connection_specific')
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '//device_specific')
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '//connection_specific//serial')
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '//connection_specific//QIS')
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '//connection_specific//usb_libs')
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)
folder2add = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]) + '//config_files')
if folder2add not in sys.path:
    sys.path.insert(0, folder2add)
from debug.versionCompare import requiredQuarchpyVersion
from device import quarchDevice
import connection_specific.connection_QIS as qisInterface
import connection_specific.connection_QPS as qpsInterface
from qis.qisFuncs import isQisRunning, startLocalQis
import qis.qisFuncs as closeQIS
import device.quarchPPM as quarchPPM
from iometer.iometerFuncs import generateIcfFromCsvLineData, readIcfCsvLineData, generateIcfFromConf, runIOMeter, processIometerInstResults
import device.quarchQPS as quarchQPS
from qps.qpsFuncs import isQpsRunning, startLocalQps, GetQpsModuleSelection
import qps.qpsFuncs as closeQPS
import disk_test.DiskTargetSelection as GetDiskTargetSelection
import qps.qpsFuncs as adjustTime
from fio.FIO_interface import runFIO
import device.scanDevices as scanDevices
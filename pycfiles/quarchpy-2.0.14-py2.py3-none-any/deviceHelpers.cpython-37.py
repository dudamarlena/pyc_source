# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\calibration\deviceHelpers.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 3326 bytes
import time, socket

def returnMeasurement(myDevice, commandString):
    valueStr = None
    unitStr = None
    responseStr = myDevice.sendCommand(commandString)
    pos = responseStr.find(' ')
    if pos != -1:
        valStr = responseStr[pos:].strip()
        unitStr = responseStr[:pos].strip()
        try:
            floatVal = float(valStr)
        except:
            raise ValueError('Response does not parse to a measurement value: ' + responseStr)

    else:
        if responseStr.find('0x') != -1:
            unitStr = 'hex'
            try:
                unitVal = int(responseStr[2:].strip(), 16)
            except:
                raise ValueError('Response does not parse to a register measurement value: ' + responseStr)

        else:
            try:
                floatVal = float(responseStr)
            except:
                for i, c in enumerate(responseStr):
                    if c.isalpha():
                        pos = i
                        break

                if i < len(responseStr):
                    valStr = responseStr[:pos].strip()
                    unitStr = responseStr[pos:].strip()
                    try:
                        floatVal = float(valStr)
                    except:
                        raise ValueError('Response does not parse to a measurement value: ' + responseStr)

                else:
                    raise ValueError('Response does not parse to a measurement value: ' + responseStr)

            return (valStr, unitStr)


class MdnsListener:

    def __init__(self):
        self.deviceList = {}

    def remove_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            addr = socket.inet_ntoa(info.address)
            self.deviceList[addr] = info.name


def locateMdnsInstr(instrName, scanTime=2):
    from zeroconf import ServiceBrowser, Zeroconf
    foundDevices = {}
    zeroconf = Zeroconf()
    listener = MdnsListener()
    browser = ServiceBrowser(zeroconf, '_http._tcp.local.', listener)
    time.sleep(scanTime)
    zeroconf.close()
    for k, v in listener.deviceList.items():
        if instrName.upper() in v.upper():
            foundDevices[k] = v

    sortedFoundDevices = {}
    for k in sorted((foundDevices.keys()), key=(lambda x: x.lower())):
        sortedFoundDevices[k] = foundDevices[k]

    return sortedFoundDevices
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\device\scanDevices.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 17509 bytes
import time, socket, sys, operator
from quarchpy.user_interface import *
from quarchpy.user_interface import User_interface
try:
    from quarchpy.connection_specific.connection_USB import importUSB
except:
    printText('System Compatibility issue - Is your Python architecture consistent with the Operating System?')

from quarchpy.device import quarchDevice, quarchArray
from quarchpy.connection_specific.connection_Serial import serialList, serial
from quarchpy.device.quarchArray import isThisAnArrayController
from quarchpy.connection_specific.connection_USB import TQuarchUSB_IF
from quarchpy.connection_specific import connection_ReST
from quarchpy.utilities import TestCenter

def mergeDict(x, y):
    if y is None:
        return x
    merged = x.copy()
    merged.update(y)
    return merged


def list_serial(debuPrint=False):
    serial_ports = serialList.comports()
    serial_modules = dict()
    for i in serial_ports:
        try:
            ser = serial.Serial((i[0]), 19200, timeout=0.5)
            ser.write(b'*serial?\r\n')
            s = ser.read(size=64)
            serial_module = s.splitlines()[1]
            serial_module = str(serial_module).replace("'", '').replace('b', '')
            if 'QTL' not in serial_module:
                serial_module = 'QTL' + serial_module
            module = (str(i[0]), str(serial_module))
            if serial_module[7] == '-':
                if serial_module[10] == '-':
                    serial_modules['SERIAL:' + str(i[0])] = serial_module
            ser.close()
        except:
            pass

    return serial_modules


def list_USB(debuPrint=False):
    QUARCH_VENDOR_ID = 5840
    QUARCH_PRODUCT_ID1 = 1097
    usb1 = importUSB()
    context = usb1.USBContext()
    usb_list = context.getDeviceList()
    if debuPrint:
        printText(usb_list)
    usb_modules = dict()
    hdList = []
    for i in usb_list:
        if hex(i.device_descriptor.idVendor) == hex(QUARCH_VENDOR_ID) and hex(i.device_descriptor.idProduct) == hex(QUARCH_PRODUCT_ID1):
            try:
                i_handle = i.open()
            except:
                if debuPrint:
                    printText('FAIL - Module detected but handle will not open')
                usb_modules['USB:???'] = 'LOCKED MODULE'
                continue

            try:
                module_sn = i_handle.getASCIIStringDescriptor(3)
                if '1944' in module_sn:
                    hdList.append(i)
            except:
                if debuPrint:
                    printText('FAIL - Module detected but unable to get serial number')
                usb_modules['USB:???'] = 'LOCKED MODULE'
                continue

            try:
                if debuPrint:
                    printText(i_handle.getASCIIStringDescriptor(3) + ' ' + i_handle.getASCIIStringDescriptor(2) + ' ' + i_handle.getASCIIStringDescriptor(1))
            except:
                if debuPrint:
                    printText('FAIL - Module detected but unable to get descriptors')
                usb_modules['USB:???'] = 'LOCKED MODULE'
                continue

            if 'QTL' not in module_sn:
                module_sn = 'QTL' + module_sn.strip()
            else:
                module_sn = module_sn.strip()
            if debuPrint:
                printText(module)
            usb_modules['USB:' + module_sn] = module_sn
            try:
                i_handle.close()
            except:
                continue

    for module in hdList:
        QquarchDevice = None
        quarchDevice = None
        quarchDevice = module
        QquarchDevice = TQuarchUSB_IF(context)
        QquarchDevice.connection = quarchDevice
        QquarchDevice.OpenPort()
        time.sleep(0.02)
        QquarchDevice.SetTimeout(2000)
        serialNo = QquarchDevice.RunCommand('*serial?').replace('\r\n', '')
        enclNo = QquarchDevice.RunCommand('*enclosure?').replace('\r\n', '')
        keyToFind = 'USB:QTL' + serialNo
        if keyToFind in usb_modules:
            del usb_modules[keyToFind]
            usb_modules['USB:QTL' + enclNo] = 'QTL' + enclNo
        QquarchDevice.ClosePort()
        QquarchDevice.deviceHandle = None

    return usb_modules


def list_network(target_conn='all', debugPring=False, lanTimeout=1, ipAddressLookup=None):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    mySocket.settimeout(lanTimeout)
    lan_modules = dict()
    specifiedDevice = None
    if ipAddressLookup is not None:
        specifiedDevice = lookupDevice(str(ipAddressLookup).strip(), mySocket, lan_modules)
    mySocket.sendto(b'Discovery: Who is out there?\x00\n', ('255.255.255.255', 30303))
    counter = 0
    while 1:
        network_modules = {}
        counter += 1
        try:
            msg_received = mySocket.recvfrom(256)
        except:
            if specifiedDevice is not None:
                msg_received = specifiedDevice
                specifiedDevice = None
            else:
                break

        cont = 0
        splits = msg_received[0].split(b'\r\n')
        del splits[-1]
        for lines in splits:
            if cont <= 1:
                index = cont
                data = repr(lines).replace("'", '').replace('b', '')
                cont += 1
            else:
                index = repr(lines[0]).replace("'", '')
                data = repr(lines[1:]).replace("'", '').replace('b', '')
            network_modules[index] = data

        module_name = get_user_level_serial_number(network_modules)
        ip_module = msg_received[1][0].strip()
        try:
            if 'QTL' not in module_name.decode('utf-8'):
                module_name = 'QTL' + module_name.decode('utf-8')
        except:
            if 'QTL' not in module_name:
                module_name = 'QTL' + module_name

        if not target_conn.lower() == 'all':
            if target_conn.lower() == 'telnet':
                if network_modules.get('\\x8a') or network_modules.get('138'):
                    lan_modules['TELNET:' + ip_module] = module_name
            if target_conn.lower() == 'all' or target_conn.lower() == 'rest':
                if network_modules.get('\\x84') or network_modules.get('132'):
                    lan_modules['REST:' + ip_module] = module_name
            if target_conn.lower() == 'all' or target_conn.lower() == 'tcp':
                if network_modules.get('\\x85') or network_modules.get('133'):
                    lan_modules['TCP:' + ip_module] = module_name

    mySocket.close()
    return lan_modules


def get_user_level_serial_number(network_modules):
    list_of_multi_module_units = [
     '1995']
    if '134' in network_modules.keys():
        module_name = network_modules.get('134').strip()
        for module in list_of_multi_module_units:
            if module in module_name:
                module_name += '-' + network_modules.get('135').strip()
                break

    else:
        if '\\x86' in network_modules.keys():
            module_name = network_modules.get('\\x86').strip()
            for module in list_of_multi_module_units:
                if module in module_name:
                    module_name += '-' + network_modules.get('\\x87').strip()
                    break

        else:
            if '131' in network_modules.keys():
                module_name = module_name = network_modules.get('131').strip()
            else:
                if '\\x83' in network_modules.keys():
                    module_name = module_name = network_modules.get('\\x83').strip()
    return module_name


def lookupDevice--- This code section failed: ---

 L. 270         0  SETUP_EXCEPT         90  'to 90'

 L. 271         2  LOAD_GLOBAL              printText
                4  LOAD_STR                 'Ipaddress lookup '
                6  LOAD_FAST                'ipAddressLookup'
                8  BINARY_ADD       
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  POP_TOP          

 L. 273        14  LOAD_FAST                'mySocket'
               16  LOAD_METHOD              sendto
               18  LOAD_CONST               b'Discovery: Who is out there?\x00\n'
               20  LOAD_GLOBAL              str
               22  LOAD_FAST                'ipAddressLookup'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  LOAD_METHOD              strip
               28  CALL_METHOD_0         0  '0 positional arguments'
               30  LOAD_CONST               30303
               32  BUILD_TUPLE_2         2 
               34  CALL_METHOD_2         2  '2 positional arguments'
               36  POP_TOP          

 L. 274        38  LOAD_FAST                'mySocket'
               40  LOAD_METHOD              recvfrom
               42  LOAD_CONST               256
               44  CALL_METHOD_1         1  '1 positional argument'
               46  STORE_FAST               'specifiedDevice'

 L. 276        48  LOAD_STR                 '\\x8a'
               50  POP_JUMP_IF_TRUE     76  'to 76'
               52  LOAD_STR                 '138'
               54  POP_JUMP_IF_TRUE     76  'to 76'
               56  LOAD_STR                 '\\x84'
               58  POP_JUMP_IF_TRUE     76  'to 76'
               60  LOAD_STR                 '132'
               62  POP_JUMP_IF_TRUE     76  'to 76'
               64  LOAD_STR                 '\\x85'
               66  POP_JUMP_IF_TRUE     76  'to 76'
               68  LOAD_STR                 '133'
               70  LOAD_FAST                'specifiedDevice'
               72  COMPARE_OP               not-in
               74  POP_JUMP_IF_FALSE    82  'to 82'
             76_0  COME_FROM            66  '66'
             76_1  COME_FROM            62  '62'
             76_2  COME_FROM            58  '58'
             76_3  COME_FROM            54  '54'
             76_4  COME_FROM            50  '50'

 L. 278        76  LOAD_CONST               None
               78  STORE_FAST               'specifiedDevice'
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM            74  '74'

 L. 281        82  LOAD_FAST                'specifiedDevice'
               84  RETURN_VALUE     
             86_0  COME_FROM            80  '80'
               86  POP_BLOCK        
               88  JUMP_FORWARD        148  'to 148'
             90_0  COME_FROM_EXCEPT      0  '0'

 L. 282        90  DUP_TOP          
               92  LOAD_GLOBAL              Exception
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   146  'to 146'
               98  POP_TOP          
              100  STORE_FAST               'e'
              102  POP_TOP          
              104  SETUP_FINALLY       134  'to 134'

 L. 283       106  LOAD_GLOBAL              printText
              108  LOAD_STR                 'Error during UDP lookup '
              110  LOAD_GLOBAL              str
              112  LOAD_FAST                'e'
              114  CALL_FUNCTION_1       1  '1 positional argument'
              116  BINARY_ADD       
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  POP_TOP          

 L. 284       122  LOAD_GLOBAL              printText
              124  LOAD_STR                 'Is the IP address correct?\r\n'
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  POP_TOP          

 L. 286       130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM_FINALLY   104  '104'
              134  LOAD_CONST               None
              136  STORE_FAST               'e'
              138  DELETE_FAST              'e'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM            96  '96'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM            88  '88'

 L. 288       148  LOAD_FAST                'specifiedDevice'
              150  LOAD_CONST               None
              152  COMPARE_OP               is
          154_156  POP_JUMP_IF_FALSE   298  'to 298'

 L. 289       158  SETUP_EXCEPT        242  'to 242'

 L. 290       160  LOAD_GLOBAL              connection_ReST
              162  LOAD_METHOD              ReSTConn
              164  LOAD_GLOBAL              str
              166  LOAD_FAST                'ipAddressLookup'
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  LOAD_METHOD              replace
              172  LOAD_STR                 '\r\n'
              174  LOAD_STR                 ''
              176  CALL_METHOD_2         2  '2 positional arguments'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  STORE_FAST               'restCon'

 L. 291       182  LOAD_FAST                'restCon'
              184  LOAD_METHOD              sendCommand
              186  LOAD_STR                 '*serial?'
              188  CALL_METHOD_1         1  '1 positional argument'
              190  STORE_FAST               'restDevice'

 L. 292       192  LOAD_GLOBAL              str
              194  LOAD_FAST                'restDevice'
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  LOAD_METHOD              startswith
              200  LOAD_STR                 'QTL'
              202  CALL_METHOD_1         1  '1 positional argument'
              204  POP_JUMP_IF_TRUE    214  'to 214'

 L. 293       206  LOAD_STR                 'QTL'
              208  LOAD_FAST                'restDevice'
              210  BINARY_ADD       
              212  STORE_FAST               'restDevice'
            214_0  COME_FROM           204  '204'

 L. 295       214  LOAD_FAST                'restDevice'
              216  LOAD_FAST                'lan_modules'
              218  LOAD_STR                 'REST:'
              220  LOAD_GLOBAL              str
              222  LOAD_FAST                'ipAddressLookup'
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  LOAD_METHOD              replace
              228  LOAD_STR                 '\r\n'
              230  LOAD_STR                 ''
              232  CALL_METHOD_2         2  '2 positional arguments'
              234  BINARY_ADD       
              236  STORE_SUBSCR     
              238  POP_BLOCK        
              240  JUMP_FORWARD        294  'to 294'
            242_0  COME_FROM_EXCEPT    158  '158'

 L. 297       242  DUP_TOP          
              244  LOAD_GLOBAL              Exception
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   292  'to 292'
              252  POP_TOP          
              254  STORE_FAST               'e'
              256  POP_TOP          
              258  SETUP_FINALLY       280  'to 280'

 L. 298       260  LOAD_GLOBAL              printText
              262  LOAD_STR                 'Error During REST scan '
              264  LOAD_GLOBAL              str
              266  LOAD_FAST                'e'
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  BINARY_ADD       
              272  CALL_FUNCTION_1       1  '1 positional argument'
              274  POP_TOP          
              276  POP_BLOCK        
              278  LOAD_CONST               None
            280_0  COME_FROM_FINALLY   258  '258'
              280  LOAD_CONST               None
              282  STORE_FAST               'e'
              284  DELETE_FAST              'e'
              286  END_FINALLY      
              288  POP_EXCEPT       
              290  JUMP_FORWARD        294  'to 294'
            292_0  COME_FROM           248  '248'
              292  END_FINALLY      
            294_0  COME_FROM           290  '290'
            294_1  COME_FROM           240  '240'

 L. 301       294  LOAD_CONST               None
              296  RETURN_VALUE     
            298_0  COME_FROM           154  '154'

Parse error at or near `JUMP_FORWARD' instruction at offset 80


def scanDevices(target_conn='all', debugPrint=False, lanTimeout=1, scanInArray=True, favouriteOnly=True, filterStr=None, ipAddressLookup=None):
    foundDevices = dict()
    scannedArrays = list()
    if target_conn.lower() == 'all':
        foundDevices = list_USB()
        foundDevices = mergeDict(foundDevices, list_serial())
        foundDevices = mergeDict(foundDevices, list_network('all', ipAddressLookup=ipAddressLookup))
    if target_conn.lower() == 'serial':
        foundDevices = list_serial()
    if target_conn.lower() == 'usb':
        foundDevices = list_USB()
    if target_conn.lower() == 'tcp' or target_conn.lower() == 'rest' or target_conn.lower() == 'telnet':
        foundDevices = list_network(target_conn, ipAddressLookup=ipAddressLookup)
    if scanInArray:
        for k, v in foundDevices.items():
            if v not in scannedArrays:
                scannedArrays.append(v)
                if isThisAnArrayController(v):
                    try:
                        scanDevice = quarchDevice(k)
                        scanArray = quarchArray(scanDevice)
                        scanDevices = scanArray.scanSubModules()
                        foundDevices = mergeDict(foundDevices, scanDevices)
                    except:
                        printText('Device in use.')
                        foundDevices[k] = 'DEVICE IN USE'

    if favouriteOnly:
        index = 0
        sortedFoundDevices = {}
        conPref = ['USB', 'TCP', 'SERIAL', 'REST', 'TELNET']
        while len(sortedFoundDevices) != len(foundDevices):
            for k, v in foundDevices.items():
                if conPref[index] in k:
                    sortedFoundDevices[k] = v

            index += 1

        foundDevices = sortedFoundDevices
        favConFoundDevices = {}
        index = 0
        for k, v in sortedFoundDevices.items():
            if not favConFoundDevices == {}:
                if v not in favConFoundDevices.values():
                    pass
                favConFoundDevices[k] = v

        foundDevices = favConFoundDevices
    sortedFoundDevices = {}
    sortedFoundDevices = sorted((foundDevices.items()), key=(operator.itemgetter(1)))
    foundDevices = dict(sortedFoundDevices)
    if filterStr != None:
        filteredDevices = {}
        for k, v in foundDevices.items():
            for j in filterStr:
                if not j in v:
                    if 'LOCKED MODULE' in v:
                        pass
                    filteredDevices[k] = v

        foundDevices = filteredDevices
    return foundDevices


def listDevices(scanDictionary):
    if not scanDictionary:
        printText('No quarch devices found to display')
    else:
        x = 1
        for k, v in scanDictionary.items():
            printText('{0:>3}'.format(str(x)) + ' - ' + '{0:<18}'.format(v) + '\t' + k)
            x += 1


def userSelectDevice(scanDictionary=None, scanFilterStr=None, favouriteOnly=True, message=None, title=None, nice=False, additionalOptions=None, target_conn='all'):
    if User_interface.instance != None:
        if User_interface.instance.selectedInterface == 'testcenter':
            nice = False
    if message is None:
        message = 'Please select a quarch device'
    if title is None:
        title = 'Select a Device'
    while True:
        if scanDictionary is None:
            printText('Scanning for devices...')
            scanDictionary = scanDevices(filterStr=scanFilterStr, favouriteOnly=favouriteOnly, target_conn=target_conn)
        else:
            if len(scanDictionary) < 1:
                scanDictionary['***No Devices Found***'] = '***No Devices Found***'
            if nice:
                if additionalOptions is None:
                    additionalOptions = [
                     'Rescan', 'Quit']
                tempList = []
                tempEl = []
                for k, v in scanDictionary.items():
                    tempEl = []
                    tempEl.append(v)
                    charPos = k.find(':')
                    tempEl.append(k)
                    tempList.append(tempEl)

                adOp = []
                for option in additionalOptions:
                    adOp.append([option] * 2)

                userStr = listSelection(title, message, tempList, additionalOptions=adOp, indexReq=True, nice=nice, tableHeaders=['Selection', 'Description'])
                userStr = userStr[2]
            else:
                devicesString = []
                for k, v in scanDictionary.items():
                    charPos = k.find(':')
                    devicesString.append(k + '=' + v + ': ' + k[:charPos])

                devicesString = ','.join(devicesString)
                if additionalOptions is None:
                    additionalOptions = 'Rescan=Rescan,Quit=Quit'
            userStr = listSelection(title=title, message=message, selectionList=devicesString, additionalOptions=additionalOptions)
        if userStr.lower() in 'quit':
            return 'quit'
        if userStr.lower() in 'rescan':
            scanDictionary = None
            favouriteOnly = True
        elif userStr.lower() in 'all conn types':
            scanDictionary = None
            favouriteOnly = False
        else:
            return userStr
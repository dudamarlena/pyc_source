# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pi/Desktop/tests/lib/python2.7/site-packages/uuidreader/__init__.py
# Compiled at: 2017-07-29 03:54:40
import evdev, utils
rfidcodes = {2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9', 11: '0'}

def init_divice(device, debug=False):
    try:
        device = evdev.InputDevice('/dev/input/event' + str(device))
        utils.debug_print('Device file found', debug)
        return device
    except:
        utils.debug_print('No Device file found', debug)
        return

    return


def read_rfid_reader(device_id, debug=False):
    print 'Read RFID form USB Card Reader'
    rfid_code = ''
    card_reader_device = init_divice(device_id, debug)
    if card_reader_device is not None:
        card_reader_device.grab()
        for event in card_reader_device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.value == 1:
                    if event.code == 28:
                        break
                    else:
                        rfid_code += rfidcodes[event.code]

        card_reader_device.ungrab()
    return rfid_code


def list_devices(debug=False):
    """
    List all connectet devices and wirte the importen information in a list
    :param debug: if True print debug msg
    :return: return a list of all usb devices
    """
    device_list = list()
    devices = [ evdev.InputDevice(fn) for fn in evdev.list_devices() ]
    if len(devices) == 0:
        utils.debug_print('No Devices found', debug)
        return list()
    for device in devices:
        utils.debug_print(str(device.fn) + ' ' + device.name + ' ' + str(device.phys), debug)
        device_list.append({'fn': device.fn, 
           'name': device.name, 
           'phys': device.phys})

    return device_list


def read(device_id, debug=False):
    """Read from the card Reader

    :param debug: if True print debug msg
    :return:  return the reading UUID
    """
    rfid_code = read_rfid_reader(device_id, debug)
    rfid_uuid = utils.rfid_code_to_uuid(rfid_code, debug)
    utils.debug_print('RFID as UUID: ' + rfid_uuid, debug)
    return rfid_uuid
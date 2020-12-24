# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fw/development/AutoBuddy/aioouimeaux/aioouimeaux/__main__.py
# Compiled at: 2018-11-10 22:21:13
# Size of source mod 2**32: 8854 bytes
import sys, asyncio as aio
from functools import partial
import argparse, socket, asyncio as aio
from aioouimeaux.wemo import WeMo
from collections import OrderedDict
wemodoi = None
listoffunc = OrderedDict()
listoffunc['Get Home Id'] = (lambda dev: dev.basicevent.GetHomeId(), 'HomeId')
listoffunc['Get MAC Address'] = (lambda dev: dev.basicevent.GetMacAddr(), 'MacAddr')
listoffunc['Get Device Id'] = (lambda dev: dev.basicevent.GetDeviceId(), '')
listoffunc['Get Serial Number'] = (lambda dev: dev.serialnumber, '')
listoffunc['Get Power Consumption'] = (lambda dev: dev.insight_params, '')

async def showinfo(future, info, dev, key=''):
    try:
        await aio.wait_for(future, timeout=5)
        resu = future.result()
        if key:
            print('\n{}: {} is {}'.format(dev.name, info, resu[key]))
        else:
            print('\n{}: {} is {}'.format(dev.name, info, resu))
    except Exception as e:
        print('\nException for {}: {} failed with {}'.format(dev.name, info, e))
        unregister_device(dev)


async def await_result(future, dev):
    try:
        await aio.wait_for(future, timeout=5)
        resu = future.result()
    except Exception as e:
        print('\nException for {}: On/Off failed with {e}'.format(dev.name))
        unregister_device(dev)


def readin():
    """Reading from stdin and displaying menu"""
    global MyWeMo
    global wemodoi
    selection = sys.stdin.readline().strip('\n')
    devices = MyWeMo.list_devices()
    devices.sort()
    lov = [x for x in selection.split(' ') if x != '']
    if lov:
        if wemodoi:
            selection = int(lov[0])
            if selection < 0:
                print('Invalid selection.')
            else:
                if wemodoi.device_type == 'Switch':
                    if selection == 1:
                        if len(lov) > 1:
                            if lov[1].lower() in ('1', 'on', 'true'):
                                future = wemodoi.on()
                            else:
                                future = wemodoi.off()
                            xx = aio.ensure_future(await_result(future, wemodoi))
                            wemodoi = None
                        else:
                            print('Error: For power you must indicate on or off\n')
                    selection -= 1
            if selection > len(listoffunc) + 2:
                print('Invalid selection.')
            else:
                if selection == len(listoffunc) + 1:
                    print('Function supported by {}'.format(wemodoi.name))
                    wemodoi.explain(prefix='\t')
                    wemodoi = None
                else:
                    if selection == len(listoffunc) + 2:
                        if len(lov) > 1:
                            lok = [x.strip() for x in lov[1].strip().split('.')]
                            fcnt = wemodoi
                            for key in lok:
                                fcnt = getattr(fcnt, key, None)
                                if fcnt is None:
                                    print('Unknown function {}'.format(lov[1].strip()))
                                    break

                            if fcnt:
                                if callable(fcnt):
                                    param = {}
                                    if len(lov) > 2:
                                        param = {}
                                        key = None
                                        for x in range(2, len(lov)):
                                            if key:
                                                param[key] = lov[x]
                                                key = None
                                            else:
                                                key = lov[x]

                                        if key:
                                            param[key] = ''
                                    if param:
                                        future = fcnt(**param)
                                    else:
                                        future = fcnt()
                                    xx = aio.ensure_future(showinfo(future, '.'.join(lok), wemodoi, ''))
                                else:
                                    print(getattr(wemodoi, fcnt, None))
                                wemodoi = None
                        else:
                            print('We need a function to execute')
                    else:
                        if selection > 0:
                            what = [x for x in listoffunc.keys()][(selection - 1)]
                            fcnt, key = listoffunc[what]
                            what = what.replace('Get', '').strip()
                            try:
                                future = fcnt(wemodoi)
                                if aio.isfuture(future):
                                    xx = aio.ensure_future(showinfo(future, what, wemodoi, key))
                            except:
                                print('Operation not supported by device.')
                            else:
                                print('\n{}: {} is {}'.format(wemodoi.name, what, future))
                            wemodoi = None
                        else:
                            wemodoi = None
        else:
            try:
                if int(lov[0]) > 0:
                    devices = MyWeMo.list_devices()
                    devices.sort()
                    if int(lov[0]) <= len(devices):
                        wemodoi = MyWeMo.devices[devices[(int(lov[0]) - 1)]]
                    else:
                        print('\nError: Not a valid selection.\n')
            except:
                print('\nError: Selection must be a number.\n')

    if wemodoi:
        print('Select Function for {}:'.format(wemodoi.name))
        selection = 1
        if wemodoi.device_type == 'Switch':
            print('\t[{}]\tPower (0 or 1)'.format(selection))
            selection += 1
        for x in listoffunc:
            print('\t[{}]\t{}'.format(selection, x))
            selection += 1

        print('\t[{}]\tExplain'.format(selection))
        print("\t[{}]\tFunction X (e.g. basicevent.GetHomeInfo see 'explain')".format(selection + 1))
        print('')
        print('\t[0]\tBack to device selection')
    else:
        idx = 1
        print('Select Device:')
        devices = MyWeMo.list_devices()
        devices.sort()
        for x in devices:
            print('\t[{}]\t{}'.format(idx, x))
            idx += 1

    print('')
    print('Your choice: ', end='', flush=True)


def report_status(dev):
    print('{} {} status is now {}'.format(dev.device_type, dev.name, dev.get_state() and 'On' or 'Off'))


def register_device(dev):
    dev.register_callback('statechange', report_status)


def unregister_device(dev):
    print('Device {} with {}'.format(dev, dev.basicevent.eventSubURL))
    MyWeMo.device_gone(dev)


loop = aio.get_event_loop()
MyWeMo = WeMo(callback=register_device)
MyWeMo.start()
try:
    try:
        loop.add_reader(sys.stdin, readin)
        print('Hit "Enter" to start')
        print('Use Ctrl-C to quit')
        loop.run_forever()
    except KeyboardInterrupt:
        print('\n', "Exiting at user's request")

finally:
    loop.remove_reader(sys.stdin)
    MyWeMo.stop()
    loop.run_until_complete(aio.sleep(1))
    loop.close()
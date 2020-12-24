# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/with_BaroboCtx_sfp/buttonCallback.py
# Compiled at: 2014-09-16 14:39:13
from barobo import Linkbot, Dongle
import time, sys
if sys.version_info[0] == 3:
    raw_input = input

def callback(mask, buttons, userdata):
    print('Button press! mask: {0} buttons: {1}'.format(hex(mask), hex(buttons)))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {0} <Com_Port> [Linkbot Serial ID]'.format(sys.argv[0]))
        quit()
    if len(sys.argv) == 3:
        serialID = sys.argv[2]
    else:
        serialID = None
    dongle = Dongle()
    dongle.connectDongleSFP(sys.argv[1])
    linkbot = dongle.getLinkbot(serialID)
    linkbot.enableButtonCallback(callback)
    raw_input('Button callbacks have been enabled. Press buttons on the Linkbot. Hit Enter when done')
# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/with_BaroboCtx_sfp/testLinkPod.py
# Compiled at: 2014-09-16 14:39:13
from barobo import Linkbot, Dongle
import barobo, time, sys, math
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
    print('Getting ADC values...')
    adcs = map(linkbot.getBreakoutADCVolts, [0, 1, 2, 3, 6, 7])
    print(list(adcs))
    print('Checking digital I/O...')
    map(lambda pin: linkbot.setBreakoutPinMode(pin, barobo.PINMODE_INPUT), range(2, 14))
    linkbot.setBreakoutPinMode(2, barobo.PINMODE_OUTPUT)
    linkbot.setBreakoutPinMode(7, barobo.PINMODE_OUTPUT)
    linkbot.setBreakoutPinMode(12, barobo.PINMODE_OUTPUT)
    linkbot.setBreakoutDigitalPin(2, 0)
    linkbot.setBreakoutDigitalPin(7, 0)
    linkbot.setBreakoutDigitalPin(12, 0)
    assert linkbot.getBreakoutDigitalPin(4) == 0
    assert linkbot.getBreakoutDigitalPin(8) == 0
    assert linkbot.getBreakoutDigitalPin(13) == 0
    linkbot.setBreakoutDigitalPin(2, 1)
    linkbot.setBreakoutDigitalPin(7, 1)
    linkbot.setBreakoutDigitalPin(12, 1)
    assert linkbot.getBreakoutDigitalPin(4) == 1
    assert linkbot.getBreakoutDigitalPin(8) == 1
    assert linkbot.getBreakoutDigitalPin(13) == 1
    map(lambda pin: linkbot.setBreakoutPinMode(pin, barobo.PINMODE_INPUT), range(2, 14))
    linkbot.setBreakoutPinMode(4, barobo.PINMODE_OUTPUT)
    linkbot.setBreakoutPinMode(8, barobo.PINMODE_OUTPUT)
    linkbot.setBreakoutPinMode(13, barobo.PINMODE_OUTPUT)
    linkbot.setBreakoutDigitalPin(4, 0)
    linkbot.setBreakoutDigitalPin(8, 0)
    linkbot.setBreakoutDigitalPin(13, 0)
    assert linkbot.getBreakoutDigitalPin(2) == 0
    assert linkbot.getBreakoutDigitalPin(7) == 0
    assert linkbot.getBreakoutDigitalPin(12) == 0
    linkbot.setBreakoutDigitalPin(4, 1)
    linkbot.setBreakoutDigitalPin(8, 1)
    linkbot.setBreakoutDigitalPin(13, 1)
    assert linkbot.getBreakoutDigitalPin(2) == 1
    assert linkbot.getBreakoutDigitalPin(7) == 1
    assert linkbot.getBreakoutDigitalPin(12) == 1
    print('Digital I/O test passed.')
    print('Checking PWM...')
    map(lambda pin: linkbot.setBreakoutPinMode(pin, barobo.PINMODE_OUTPUT), [3, 5, 6, 9, 10, 11])
    t = 0.0
    for i in range(0, 50):
        map(lambda pin: linkbot.setBreakoutAnalogPin(pin, int(127 * math.sin(t * 3)) + 127), [3, 5, 6, 9, 10, 11])
        time.sleep(0.1)
        t += 0.1
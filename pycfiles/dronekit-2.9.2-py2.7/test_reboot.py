# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_reboot.py
# Compiled at: 2019-03-14 01:22:55
from nose.tools import assert_equal
from dronekit import connect
from dronekit.test import with_sitl
import time

@with_sitl
def test_reboot(connpath):
    """Tries to reboot the vehicle, and checks that the autopilot ACKs the command."""
    vehicle = connect(connpath, wait_ready=True)
    reboot_acks = []

    def on_ack(self, name, message):
        if message.command == 246:
            reboot_acks.append(message)

    vehicle.add_message_listener('COMMAND_ACK', on_ack)
    vehicle.reboot()
    time.sleep(0.5)
    vehicle.remove_message_listener('COMMAND_ACK', on_ack)
    assert_equal(1, len(reboot_acks))
    assert_equal(246, reboot_acks[0].command)
    assert_equal(0, reboot_acks[0].result)
    vehicle.close()
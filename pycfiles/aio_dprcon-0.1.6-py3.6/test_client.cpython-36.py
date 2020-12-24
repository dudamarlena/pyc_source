# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_client.py
# Compiled at: 2017-12-10 15:37:02
# Size of source mod 2**32: 1150 bytes
import asyncio, time

def test_connect_once(loop, rcon_client, dummy_status):

    async def __send_status_data(c):
        await asyncio.sleep(0.5)
        c.cmd_data_received(dummy_status, (c.remote_host, c.remote_port))
        await asyncio.sleep(1)

    if not rcon_client.loop is loop:
        raise AssertionError
    else:
        loop.run_until_complete(asyncio.gather((rcon_client.connect_once()), (__send_status_data(rcon_client)),
          loop=loop))
        time.sleep(1)
        assert loop.create_datagram_endpoint.called
        assert rcon_client.connected


def test_connect_forever(loop, rcon_client, dummy_status):
    assert rcon_client.loop is loop

    async def __send_status_data(c):
        await asyncio.sleep(0.5)
        c.cmd_data_received(dummy_status, (c.remote_host, c.remote_port))
        await asyncio.sleep(5)

    tasks = [
     rcon_client.connect_forever(),
     __send_status_data(rcon_client)]
    finished, pending = loop.run_until_complete(asyncio.wait(tasks, loop=loop, return_when=(asyncio.FIRST_COMPLETED)))
    for task in pending:
        task.cancel()
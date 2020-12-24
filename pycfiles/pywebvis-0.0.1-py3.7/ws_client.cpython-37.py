# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webvis/ws_client.py
# Compiled at: 2019-11-05 21:15:15
# Size of source mod 2**32: 534 bytes
import trio
from sys import stderr
from trio_websocket import open_websocket_url

def main():
    trio.run(request)


async def request():
    try:
        async with open_websocket_url('wss://echo.websocket.org') as ws:
            print('sending message')
            await ws.send_message('hello world!')
            message = await ws.get_message()
            print('Received message: %s' % message)
    except OSError as ose:
        try:
            print(('Connection attempt failed: %s' % ose), file=stderr)
        finally:
            ose = None
            del ose


if __name__ == '__main__':
    main()
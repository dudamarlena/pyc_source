# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/helpers.py
# Compiled at: 2019-09-30 07:14:24
# Size of source mod 2**32: 1203 bytes
__doc__ = 'Various helper methods.'
import asyncio, pyatv

def auto_connect(handler, timeout=5, not_found=None):
    """Short method for connecting to a device.

    This is a convenience method that create an event loop, auto discovers
    devices, picks the first device found, connects to it and passes it to a
    user provided handler. An optional error handler can be provided that is
    called when no device was found. Very inflexible in many cases, but can be
    handys sometimes when trying things.

    Note: both handler and not_found must be coroutines
    """

    async def _handle(loop):
        atvs = await pyatv.scan_for_apple_tvs(loop,
          timeout=timeout, abort_on_found=True)
        if atvs:
            atv = await pyatv.connect_to_apple_tv(atvs[0], loop)
            try:
                await handler(atv)
            finally:
                await atv.logout()

        if not_found is not None:
            await not_found()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_handle(loop))
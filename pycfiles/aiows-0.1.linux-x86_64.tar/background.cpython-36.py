# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /hdd/dev/os/aiows/.env/lib/python3.6/site-packages/aiows/aioapp/background.py
# Compiled at: 2018-10-09 14:19:25
# Size of source mod 2**32: 263 bytes
from aiows.aioapp.queue import MessagePool

async def message_queue(app):
    """
    Initialize messages pool worker.
    :param app:
    :return:
    """
    app['mp'] = MessagePool()


tasks = (
 (
  'message_queue', message_queue),)
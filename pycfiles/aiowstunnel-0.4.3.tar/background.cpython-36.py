# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
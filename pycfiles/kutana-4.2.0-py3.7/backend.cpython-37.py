# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kutana/backend.py
# Compiled at: 2020-05-02 08:54:53
# Size of source mod 2**32: 540 bytes


class Backend:

    async def on_start(self, app):
        pass

    async def on_shutdown(self, app):
        pass

    def prepare_context(self, ctx):
        pass

    async def perform_updates_request(self, submit_update):
        raise NotImplementedError

    async def perform_send(self, target_id, message, attachments, kwargs):
        raise NotImplementedError

    async def perform_api_call(self, method, kwargs):
        raise NotImplementedError

    @classmethod
    def get_identity(cls):
        return cls.__name__.lower()
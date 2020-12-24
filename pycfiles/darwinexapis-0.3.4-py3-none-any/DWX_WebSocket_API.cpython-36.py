# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eriz/Desktop/darwinexapis/darwinexapis/API/WebSocketAPI/DWX_WebSocket_API.py
# Compiled at: 2020-05-13 05:35:55
# Size of source mod 2**32: 4665 bytes
"""
    DWX WebSocket API - Subclass of DWX_API for Quotes Streaming
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: June 25, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""
import os, time, sys, logging
logger = logging.getLogger()
from darwinexapis.API.dwx_api import DWX_API
import websockets, json, asyncio

class DWX_WebSocket_API(DWX_API):

    def __init__(self, _auth_creds='', _api_url='ws://api.darwinex.com/quotewebsocket/1.0.0', _api_name='', _version=0.0):
        self._api_url = _api_url
        self._auth_creds = _auth_creds
        self._api_name = _api_name
        self._version = _version
        super(DWX_WebSocket_API, self).__init__(self._auth_creds, self._api_url, self._api_name, self._version)
        self._active = True
        self._websocket = None

    async def subscribe(self, _symbols=[
 'DWZ.4.7', 'DWC.4.20', 'LVS.4.20', 'SYO.4.24', 'YZZ.4.20']):
        async with websockets.connect((self._api_url), extra_headers=(self._auth_headers)) as websocket:
            await websocket.send(json.dumps({'op':'subscribe',  'productNames':_symbols}))
            while self._active:
                if time.time() > self.AUTHENTICATION.expires_in:
                    logger.warning('\n[SUBSCRIBE] - The expiration time has REACHED > ¡Generate TOKENS!')
                    self.AUTHENTICATION._get_access_refresh_tokens_wrapper()
                    logger.warning('[SUBSCRIBE] - Need to re-run the loop with new TOKENS...')
                    return
                logger.warning('\n[SUBSCRIBE] - The expiration time has NOT reached yet > Continue...')
                _ret = await websocket.recv()
                logger.warning(_ret)

    def run(self, _symbols=[
 'DWZ.4.7', 'DWC.4.20', 'LVS.4.20', 'SYO.4.24', 'YZZ.4.20']):
        self._symbols = _symbols
        self.event_loop = asyncio.get_event_loop()
        try:
            self.event_loop.run_until_complete(self.subscribe(_symbols))
        except RuntimeError as ex:
            logger.warning(f"[RUNTIME ERROR] > {ex}")
        except KeyboardInterrupt:
            logger.warning('[EXCEPTION] > ¡KeyboardInterrupt Exception!')
        else:
            logger.warning('[RUN_ELSE] - Tokens generated > We will re-run the loop and start the WS connection again')
            for task in asyncio.Task.all_tasks():
                task.cancel()

            logger.warning('[RUN_ELSE] - All tasks cancelled')
            self.stop_and_close()

    def stop_and_close(self):
        """Stop and close loop"""
        self.event_loop.stop()
        self.event_loop.close()
        logger.warning('[CLOSE] - Loop stopped and closed')
        self.launch_loop_again()

    def launch_loop_again(self):
        super(DWX_WebSocket_API, self).__init__(self._auth_creds, self._api_url, self._api_name, self._version)
        asyncio.set_event_loop(asyncio.new_event_loop())
        logger.warning('[LAUNCH] - New event loop set and assigned > Will run the coroutine again..')
        self.run(_symbols=(self._symbols))
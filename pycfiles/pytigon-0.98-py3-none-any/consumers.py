# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./_schwiki/schwiki/consumers.py
# Compiled at: 2019-11-02 09:56:54
# Size of source mod 2**32: 364 bytes
import os, sys, datetime, json, asyncio
from channels.consumer import AsyncConsumer, SyncConsumer
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.generic.http import AsyncHttpConsumer
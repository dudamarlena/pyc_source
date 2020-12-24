# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/loop.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 246 bytes
import asyncio

def get_event_loop(debug=False):
    if not debug:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        asyncio.set_event_loop(uvloop.new_event_loop())
    return asyncio.get_event_loop()
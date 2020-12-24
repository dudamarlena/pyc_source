# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /hdd/dev/os/aiows/.env/lib/python3.6/site-packages/aiows/aioapp/urls.py
# Compiled at: 2018-10-05 10:06:17
# Size of source mod 2**32: 253 bytes
from aiows.aioapp import views
patterns = [
 (
  'get', ['channel/{channel}/', views.channel_subscribe]),
 (
  'post', ['channel/{channel}/', views.channel_publish]),
 (
  'post', ['broadcast/', views.channel_publish_bulk])]
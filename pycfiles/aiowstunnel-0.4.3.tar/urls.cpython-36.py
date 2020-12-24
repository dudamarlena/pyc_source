# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
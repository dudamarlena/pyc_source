# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/asyncbots/history.py
# Compiled at: 2018-01-04 18:06:59
# Size of source mod 2**32: 264 bytes
"""Mongoengine definition for storing history"""
from mongoengine import Document, StringField

class HistoryDoc(Document):
    __doc__ = 'A Slack message'
    uid = StringField()
    channel = StringField()
    text = StringField()
    time = StringField(unique=True)
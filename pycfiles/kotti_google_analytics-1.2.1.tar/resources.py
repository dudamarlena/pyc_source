# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_google_analytics/kotti_google_analytics/resources.py
# Compiled at: 2016-08-20 14:25:54
"""
Created on 2016-06-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from kotti.interfaces import IDefaultWorkflow
from kotti.resources import Content
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from zope.interface import implements
from kotti_google_analytics import _
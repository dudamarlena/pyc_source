# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/djreservation/djreservation/settings.py
# Compiled at: 2019-02-19 21:49:51
# Size of source mod 2**32: 751 bytes
"""
Free as freedom will be 5/10/2016

@author: luisza
"""
from __future__ import unicode_literals
from django.conf import settings
from django.utils import timezone
from datetime import datetime
TOKENIZE = getattr(settings, 'DJRESERVATION_TOKENIZE', False)
START_RESERVATION_DATETIME = getattr(settings, 'DJRESERVATION_START_RESERVATION_DATETIME', None)
END_RESERVATION_DATETIME = getattr(settings, 'DJRESERVATION_END_RESERVATION_DATETIME', None)
if START_RESERVATION_DATETIME:
    START_RESERVATION_DATETIME = datetime.strptime(START_RESERVATION_DATETIME, '%d/%m/%Y %H:%M')
if END_RESERVATION_DATETIME:
    END_RESERVATION_DATETIME = datetime.strptime(END_RESERVATION_DATETIME, '%d/%m/%Y %H:%M')
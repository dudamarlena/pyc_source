# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/autoforms/signal.py
# Compiled at: 2012-07-06 10:27:01
from django.dispatch import Signal
form_filled = Signal(providing_args=['form', 'instance'])
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/trytond/modules/twilio_messages/__init__.py
# Compiled at: 2018-04-26 06:40:48
from trytond.pool import Pool
from . import twilio_messages
from . import routes
__all__ = ['register', 'routes']

def register():
    Pool.register(twilio_messages.Message, twilio_messages.SendMessageStart, module='twilio_messages', type_='model')
    Pool.register(twilio_messages.SendMessage, module='twilio_messages', type_='wizard')
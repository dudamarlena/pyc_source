# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/services/chat/chatService.py
# Compiled at: 2010-06-01 14:13:33
from dust.core.util import encodeAddress

class ChatHandler:

    def __init__(self):
        pass

    def handle(self, msock, msg, addr):
        print('Message from ' + encodeAddress(addr) + ':')
        print(msg.decode('ascii'))
        print('-----------------')
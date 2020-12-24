# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/controllers/HalWebControllers.py
# Compiled at: 2012-01-05 21:48:33
from lib.halicea.HalRequestHandler import HalRequestHandler as hrh
from lib.halicea.decorators import *

class WelcomeController(hrh):

    @ClearDefaults()
    @Default('welcome')
    def SetOperations(self):
        pass

    def welcome(self):
        return {}
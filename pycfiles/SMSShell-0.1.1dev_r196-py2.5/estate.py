# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/smsshell/controllers/estate.py
# Compiled at: 2008-04-10 11:38:21
"""Estate Controller

AUTHOR Emanuel Gardaya Calso

"""
import logging
from smsshell.lib.base import *
log = logging.getLogger(__name__)

class EstateController(ListController):
    table = model.Estate
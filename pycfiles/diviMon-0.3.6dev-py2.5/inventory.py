# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/divimon/controllers/inventory.py
# Compiled at: 2008-07-30 10:44:43
import logging
from divimon.lib.base import *
from divimon import model
log = logging.getLogger(__name__)

class InventoryController(ListController):
    table = model.Inventory
    parent = dict(item=dict(table=model.Item, column='name'))
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/subicpos/controllers/sale_conv.py
# Compiled at: 2008-05-10 22:46:25
import logging
from subicpos.lib.base import *
from sale import SaleController
log = logging.getLogger(__name__)

class SaleConvController(SaleController):

    def _init_custom(self):
        c.title = 'Convenience Store Sale'

    def render_edit(self):
        return render('/sale/edit.mako')
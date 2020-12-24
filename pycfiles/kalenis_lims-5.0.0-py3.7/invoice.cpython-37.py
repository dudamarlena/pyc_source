# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims_project_tas/invoice.py
# Compiled at: 2019-01-16 10:44:04
# Size of source mod 2**32: 627 bytes
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval
__all__ = [
 'Invoice']

class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'
    lims_project = fields.Many2One('lims.project', 'TAS Project', domain=[
     ('type', '=', 'tas')],
      states={'readonly':Eval('state') != 'draft', 
     'invisible':Eval('type').in_(['in'])})
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims_project_tas/configuration.py
# Compiled at: 2019-01-16 09:41:20
# Size of source mod 2**32: 1315 bytes
from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval
__all__ = [
 'LabWorkYear', 'LabWorkYearSequence']

class LabWorkYear(metaclass=PoolMeta):
    __name__ = 'lims.lab.workyear'
    project_tas_sequence = fields.MultiValue(fields.Many2One('ir.sequence.strict',
      'TAS Projects Sequence', required=True, domain=[
     (
      'company', 'in',
      [
       Eval('context', {}).get('company', -1), None]),
     ('code', '=', 'lims.project')]))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'project_tas_sequence':
            return pool.get('lims.lab.workyear.sequence')
        return super(LabWorkYear, cls).multivalue_model(field)


class LabWorkYearSequence(metaclass=PoolMeta):
    __name__ = 'lims.lab.workyear.sequence'
    project_tas_sequence = fields.Many2One('ir.sequence.strict', 'TAS Projects Sequence',
      depends=['company'], domain=[
     (
      'company', 'in', [Eval('company', -1), None]),
     ('code', '=', 'lims.project')])
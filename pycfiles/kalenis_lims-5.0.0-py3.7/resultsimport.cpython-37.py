# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims_instrument_generic_service/resultsimport.py
# Compiled at: 2019-01-16 09:41:20
# Size of source mod 2**32: 933 bytes
from trytond.pool import PoolMeta
from . import generic_service_xls
__all__ = [
 'ResultsImport']

class ResultsImport(metaclass=PoolMeta):
    __name__ = 'lims.resultsimport'

    @classmethod
    def __setup__(cls):
        super(ResultsImport, cls).__setup__()
        controllers = [
         ('generic_service_xls', 'Generic Service Form - XLS')]
        for controller in controllers:
            if controller not in cls.name.selection:
                cls.name.selection.append(controller)

    def loadController(self):
        if self.name == 'generic_service_xls':
            self.controller = generic_service_xls
        else:
            return super(ResultsImport, self).loadController()
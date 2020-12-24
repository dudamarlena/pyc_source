# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mathml/utils/sqlterm.py
# Compiled at: 2006-02-06 02:06:09
from mathml.termbuilder import tree_converters, InfixTermBuilder
__all__ = ['SqlTermBuilder']

class SqlTermBuilder(InfixTermBuilder):
    _NAME_MAP = {'e': 'exp(1.0)', 
       'pi': 'pi()', 
       'true': 'TRUE', 
       'false': 'FALSE'}

    def _handle_const_bool(self, operator, operands, affin):
        return [
         operands[0] and 'TRUE' or 'FALSE']

    def _handle_const_complex(self, operator, operands, affin):
        raise NotImplementedError, 'Complex numbers cannot be converted to SQL.'

    def _handle_interval(self, operator, operands, affin):
        raise NotImplementedError, 'Intervals cannot be converted to SQL.'


tree_converters.register_converter('sql', SqlTermBuilder())
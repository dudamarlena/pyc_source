# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/command.py
# Compiled at: 2019-05-06 15:51:29
# Size of source mod 2**32: 2781 bytes
from norm.executable import NormExecutable
from norm.executable.schema.type import TypeName
from norm.grammar.literals import MOP
import logging
logger = logging.getLogger(__name__)

class Command(NormExecutable):

    def __init__(self, op, type_name):
        super().__init__()
        self.op = op
        self.type_name = type_name
        from norm.models import Lambda
        self.lam = None

    def compile(self, context):
        self.lam = self.type_name.lam
        return self

    def execute(self, context):
        if self.op == MOP.DESCRIBE:
            d = self.lam.data.describe().transpose()
            numerics = set(d.index)
            non_numerics = set(self.lam.data.columns).difference(numerics)
            datetimes = [col for col in non_numerics if self.lam.data[col].dtype.name.find('datetime') >= 0]
            non_numerics = non_numerics.difference(datetimes)
            for col in numerics:
                d.loc[(col, 'unique')] = self.lam.data[col].drop_duplicates().count()

            for col in non_numerics:
                d.loc[col] = [
                 self.lam.data[col].count(), None, None, None, None, None, None, None,
                 self.lam.data[col].drop_duplicates().count()]

            for col in datetimes:
                d.loc[col] = [
                 self.lam.data[col].count(), None, None, self.lam.data[col].min(), None, None, None,
                 self.lam.data[col].max(), self.lam.data[col].drop_duplicates().count()]

            for col in self.lam.data.columns:
                d.loc[(col, 'type')] = str(self.lam.get_type(col)) or 'Any'

            d['tag'] = ''
            norm_cols = [self.lam.VAR_LABEL, self.lam.VAR_TOMBSTONE, self.lam.VAR_TIMESTAMP, self.lam.VAR_PROB]
            d.loc[(norm_cols, 'tag')] = 'reserved'
            for v in self.lam.variables:
                if v.primary:
                    d.loc[(v.name, 'tag')] = 'primary'
                else:
                    d.loc[(v.name, 'tag')] = 'optional'

            d['count'] = d['count'].astype('int')
            d['unique'] = d['unique'].astype('int')
            return d.loc[(self.lam.data.columns,
             ['tag', 'type', 'count', 'unique', 'min', 'max', 'mean', 'std', '25%',
              '50%', '75%'])]
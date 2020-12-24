# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/models/python.py
# Compiled at: 2019-05-07 00:02:04
# Size of source mod 2**32: 2528 bytes
__doc__ = 'A collection of ORM sqlalchemy models for PythonLambda'
from textwrap import dedent
from pandas import DataFrame, Series
from sqlalchemy import Column, Text, orm
from norm.executable import NormError
from norm.models.norm import Lambda, Status, Variable
import logging
logger = logging.getLogger(__name__)

class PythonLambda(Lambda):
    VAR_INPUTS = 'inputs'
    code = Column(Text, default='')
    __mapper_args__ = {'polymorphic_identity': 'lambda_python'}

    def __init__(self, namespace, name, description, code):
        from norm.models import lambdas
        super().__init__(namespace=namespace, name=name,
          description=description,
          variables=[
         Variable(self.VAR_INPUTS, lambdas.Any),
         Variable(self.VAR_OUTPUT, lambdas.Any)])
        self.status = Status.READY
        self.code = dedent(code)
        self._load_func()
        self.atomic = True

    def _load_func(self):
        try:
            d = {}
            exec(self.code, d)
            self._func = d.get(self.name)
        except Exception:
            msg = 'Execution errors: \n{}'.format(self.code)
            logger.error(msg)
            raise NormError(msg)

        if not (self._func is None or callable(self._func)):
            msg = 'Function {} does not exist or failed to parse'.format(self.name)
            logger.error(msg)
            raise NormError(msg)

    @orm.reconstructor
    def init_on_load(self):
        self._load_func()

    def __call__(self, **inputs):
        inp = inputs.get(self.VAR_INPUTS)
        try:
            if inp is not None:
                df = self._func(inp)
                if isinstance(df, Series):
                    df.name = self.VAR_OUTPUT
                if isinstance(inp, DataFrame) and not isinstance(df, DataFrame):
                    raise NormError
            else:
                df = self._func()
        except Exception:
            df = DataFrame(inp.apply((self._func), axis=1), columns=[self.VAR_OUTPUT])

        return df
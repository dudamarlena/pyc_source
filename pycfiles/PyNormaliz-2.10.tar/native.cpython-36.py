# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/models/native.py
# Compiled at: 2019-05-06 23:25:40
# Size of source mod 2**32: 5417 bytes
__doc__ = 'A collection of ORM sqlalchemy models for NativeLambda'
from norm.models import Register
from norm.models.norm import Lambda, Variable, Status
from datetime import datetime
import numpy as np, logging
logger = logging.getLogger(__name__)

class NativeLambda(Lambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native'}
    NAMESPACE = 'norm.native'

    def __init__(self, name, description, variables, dtype='object'):
        super().__init__(namespace=(self.NAMESPACE), name=name,
          description=description,
          variables=variables,
          dtype=dtype)
        self.status = Status.READY
        self.atomic = True

    def empty_data(self):
        pass


@Register()
class TypeLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_type'}

    def __init__(self):
        super().__init__(name='Type', description='A logical function',
          variables=[])


@Register()
class AnyLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_any'}

    def __init__(self):
        super().__init__(name='Any', description='Any type',
          variables=[])

    @property
    def default(self):
        pass


class ListLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_list'}
    INTERN = 'intern'

    def __init__(self, type_):
        variable = Variable(self.INTERN, type_)
        super().__init__(name=('List[{}]'.format(type_.signature)), description='A list of a certain type',
          variables=[
         variable])

    @property
    def default(self):
        return []


@Register()
class BooleanLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_boolean'}

    def __init__(self):
        super().__init__(name='Boolean', description='Boolean, true/false',
          variables=[],
          dtype='bool')

    @property
    def default(self):
        return False


@Register()
class FloatLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_float'}

    def __init__(self):
        super().__init__(name='Float', description='Integer, -inf..+inf',
          variables=[],
          dtype='float')

    @property
    def default(self):
        return 0.0


@Register()
class IntegerLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_integer'}

    def __init__(self):
        super().__init__(name='Integer', description='Integer, -inf..+inf',
          variables=[],
          dtype='int')

    @property
    def default(self):
        return 0


@Register()
class StringLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_string'}

    def __init__(self):
        super().__init__(name='String', description='String, "blahbalh"',
          variables=[])

    @property
    def default(self):
        return ''


@Register()
class PatternLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_pattern'}

    def __init__(self):
        super().__init__(name='Pattern', description='Pattern, r"^test[0-9]+"',
          variables=[])

    @property
    def default(self):
        return ''


@Register()
class UUIDLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_uuid'}

    def __init__(self):
        super().__init__(name='UUID', description='UUID, $"sfsfsfsf"',
          variables=[])

    @property
    def default(self):
        return ''


@Register()
class URLLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_url'}

    def __init__(self):
        super().__init__(name='URL', description='URL, l"http://example.com"',
          variables=[])

    @property
    def default(self):
        return 'http://'


@Register()
class DatetimeLambda(NativeLambda):
    __mapper_args__ = {'polymorphic_identity': 'lambda_native_datetime'}

    def __init__(self):
        super().__init__(name='Datetime', description='Datetime, t"2018-09-01"',
          variables=[],
          dtype='datetime64[ns]')

    @property
    def default(self):
        return np.datetime64(datetime.utcnow())


def get_type_by_dtype(dtype):
    """
    Convert the numpy dtype to native lambda
    :param dtype: the numpy dtype
    :type dtype: numpy.dtype
    :return: the Lambda
    :rtype: Lambda
    """
    from norm.models import lambdas
    if dtype.name.find('int') > -1:
        return lambdas.Integer
    else:
        if dtype.name.find('float') > -1:
            return lambdas.Float
        return lambdas.Any
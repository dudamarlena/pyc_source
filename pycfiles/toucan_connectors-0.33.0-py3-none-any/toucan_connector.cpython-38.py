# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/toucan_connector.py
# Compiled at: 2020-04-14 08:50:37
# Size of source mod 2**32: 10341 bytes
import logging, operator, os, socket
from abc import ABCMeta, abstractmethod
from enum import Enum
from functools import reduce, wraps
from typing import Iterable, List, NamedTuple, Optional, Type
import pandas as pd, tenacity as tny
from pydantic import BaseModel
from toucan_connectors.common import apply_query_parameters
from toucan_connectors.pandas_translator import PandasConditionTranslator
try:
    from bearer import Bearer
except ImportError:
    pass
else:

    class DataSlice(NamedTuple):
        df: pd.DataFrame
        total_count: int


    class StrEnum(str, Enum):
        __doc__ = 'Class to easily make schemas with enum values and type string'


    def strlist_to_enum(field: str, strlist: List[str], default_value=Ellipsis) -> tuple:
        """
    Convert a list of strings to a pydantic schema enum
    the value is either <default value> or a tuple ( <type>, <default value> )
    If the field is required, the <default value> has to be '...' (cf pydantic doc)
    By default, the field is considered required.
    """
        return (
         StrEnum(field, {v:v for v in strlist}), default_value)


    class ToucanDataSource(BaseModel):
        domain: str
        name: str
        type = None
        type: str
        load = True
        load: bool
        live_data = False
        live_data: bool
        validation = None
        validation: list
        parameters = None
        parameters: dict

        class Config:
            extra = 'forbid'
            validate_assignment = True

        @classmethod
        def get_form(cls, connector: 'ToucanConnector', current_config):
            """
        Method to retrieve the form with a current config
        Once the connector is set, we are often able to enforce some values depending
        on what the current `ToucanDataSource` config looks like

        By default, we simply return the model schema.
        """
            return cls.schema()


    class RetryPolicy(BaseModel):
        __doc__ = 'Generic "retry" policy management.\n\n    This is just a declarative wrapper around `tenacity.retry` that should\n    ease retry policy definition for most classic use cases.\n\n    It can be instantiated with the following parameters:\n\n    - `retry_on`: the list of expected exception classes that should trigger a retry\n    - `max_attempts`: the maximum number of retries before giving up\n    - `max_delay`: delay, in seconds, above which we should give up\n    - `wait_time`: time, in seconds, between each retry.\n\n    The class also exposes the `retry_decorator` method that is responsible to convert\n    the parameters aforementioned in a corresponding `tenacity.retry` decorator. If\n    you need a really custom retry policy and want to use the full power of the\n    `tenacity` library, you can simply override this method and return your own\n    `tenacity.retry` decorator.\n    '
        max_attempts = 1
        max_attempts: Optional[int]
        max_delay = 0.0
        max_delay: Optional[float]
        wait_time = 0.0
        wait_time: Optional[float]

        def __init__(self, retry_on=(), logger=None, **data):
            (super().__init__)(**data)
            self.__dict__['retry_on'] = retry_on
            self.__dict__['logger'] = logger

        @property
        def tny_stop(self):
            """generate corresponding `stop` parameter for `tenacity.retry`"""
            stoppers = []
            if self.max_attempts > 1:
                stoppers.append(tny.stop_after_attempt(self.max_attempts))
            if self.max_delay:
                stoppers.append(tny.stop_after_delay(self.max_delay))
            if stoppers:
                return reduce(operator.or_, stoppers)

        @property
        def tny_retry(self):
            """generate corresponding `retry` parameter for `tenacity.retry`"""
            if self.retry_on:
                return tny.retry_if_exception_type(self.retry_on)

        @property
        def tny_wait(self):
            """generate corresponding `wait` parameter for `tenacity.retry`"""
            if self.wait_time:
                return tny.wait_fixed(self.wait_time)

        @property
        def tny_after(self):
            """generate corresponding `after` parameter for `tenacity.retry`"""
            if self.logger:
                return tny.after_log(self.logger, logging.DEBUG)

        def retry_decorator(self):
            """build the `tenaticy.retry` decorator corresponding to policy"""
            tny_kwargs = {}
            for attr in dir(self):
                if attr.startswith('tny_') and attr != 'tny_after':
                    paramvalue = getattr(self, attr)
                    if paramvalue is not None:
                        tny_kwargs[attr[4:]] = paramvalue
            else:
                if tny_kwargs:
                    if self.tny_after:
                        tny_kwargs['after'] = self.tny_after
                    return (tny.retry)(reraise=True, **tny_kwargs)

        def __call__(self, f):
            """make retry_policy instances behave as `tenacity.retry` decorators"""
            decorator = self.retry_decorator()
            if decorator:
                return decorator(f)
            return f


    def decorate_func_with_retry(func):
        """wrap `func` with the retry policy defined on the connector.
    If the retry policy is None, just leave the `get_df` implementation as is.
    """

        @wraps(func)
        def get_func_and_retry(self, *args, **kwargs):
            if self.retry_decorator:
                return (self.retry_decorator(func))(self, *args, **kwargs)
            return func(self, *args, **kwargs)

        return get_func_and_retry


    class ToucanConnector(BaseModel, metaclass=ABCMeta):
        __doc__ = 'Abstract base class for all toucan connectors.\n\n    Each concrete connector should implement the `get_df` method that accepts a\n    datasource definition and return the corresponding pandas dataframe. This\n    base class allows to specify a retry policy on the `get_df` method. The\n    default is not to retry on error but you can customize some of connector\n    model parameters to define custom retry policy.\n\n    Model parameters:\n\n\n    - `max_attempts`: the maximum number of retries before giving up\n    - `max_delay`: delay, in seconds, above which we should give up\n    - `wait_time`: time, in seconds, between each retry.\n\n    In order to retry only on some custom exception classes, you can override\n    the `_retry_on` class attribute in your concrete connector class.\n    '
        name: str
        retry_policy = RetryPolicy()
        retry_policy: Optional[RetryPolicy]
        _retry_on = ()
        _retry_on: Iterable[Type[BaseException]]
        type = None
        type: str

        class Config:
            extra = 'forbid'
            validate_assignment = True

        def __init_subclass__(cls):
            try:
                cls.data_source_model = cls.__fields__.pop('data_source_model').type_
                cls.logger = logging.getLogger(cls.__name__)
            except KeyError as e:
                try:
                    raise TypeError(f"{cls.__name__} has no {e} attribute.")
                finally:
                    e = None
                    del e

            else:
                if 'bearer_integration' in cls.__fields__:
                    cls.bearer_integration = cls.__fields__['bearer_integration'].default

        def bearer_oauth_get_endpoint(self, endpoint: str, query: Optional[dict]=None):
            """Generic method to get an endpoint for an OAuth API integrated with Bearer"""
            return Bearer(os.environ.get('BEARER_API_KEY')).integration(self.bearer_integration).auth(self.bearer_auth_id).get(endpoint,
              query=query).json()

        @property
        def retry_decorator(self):
            kwargs = {**(self.retry_policy.dict()), **{'retry_on':self._retry_on,  'logger':self.logger}}
            return RetryPolicy(**kwargs)

        @abstractmethod
        def _retrieve_data(self, data_source: ToucanDataSource):
            """Main method to retrieve a pandas dataframe"""
            pass

        @decorate_func_with_retry
        def get_df(self, data_source: ToucanDataSource, permissions: Optional[dict]=None) -> pd.DataFrame:
            """
        Method to retrieve the data as a pandas dataframe
        filtered by permissions
        """
            res = self._retrieve_data(data_source)
            if permissions is not None:
                permissions_query = PandasConditionTranslator.translate(permissions)
                permissions_query = apply_query_parameters(permissions_query, data_source.parameters)
                res = res.query(permissions_query)
            return res

        def get_slice(self, data_source: ToucanDataSource, permissions: Optional[dict]=None, offset: int=0, limit: Optional[int]=None) -> DataSlice:
            """
        Method to retrieve a part of the data as a pandas dataframe
        and the total size filtered with permissions

        - offset is the index of the starting row
        - limit is the number of rows to retrieve
        Exemple: if offset = 5 and limit = 10 then 10 results are expected from 6th row
        """
            df = self.get_df(data_source, permissions)
            if limit is not None:
                return DataSlice(df[offset:offset + limit], len(df))
            return DataSlice(df[offset:], len(df))

        def explain(self, data_source: ToucanDataSource, permissions: Optional[dict]=None):
            """Method to give metrics about the query"""
            pass

        @staticmethod
        def check_hostname(hostname):
            """Check if a hostname is resolved"""
            socket.gethostbyname(hostname)

        @staticmethod
        def check_port(host, port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as (s):
                s.connect((host, port))

        def get_status(self) -> dict:
            """
        Check if connection can be made.
        Returns
        {
          'status': True/False/None  # the status of the connection (None if no check has been made)
          'details': [(< type of check >, True/False/None), (...), ...]
          'error': < error message >  # if a check raised an error, return it
        }
        e.g.
        {
          'status': False,
          'details': [
            ('hostname resolved', True),
            ('port opened', False,),
            ('db validation', None),
            ...
          ],
          'error': 'port must be 0-65535'
        }
        """
            return {'status':None, 
             'details':[],  'error':None}
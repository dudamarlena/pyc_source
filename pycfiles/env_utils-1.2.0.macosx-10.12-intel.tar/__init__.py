# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/python-env-utils/lib/python2.7/site-packages/env_utils/__init__.py
# Compiled at: 2016-11-24 05:14:27
from dateutil import parser
import decimal, json, os

class RequiredSettingMissing(Exception):

    def __init__(self, key):
        msg = "Required env var '%s' is missing." % key
        super(RequiredSettingMissing, self).__init__(msg)


def get_env(key, default=None, coerce=lambda x: x, required=False):
    """Return env var coerced into a type other than string.

    This function extends the standard os.getenv function to enable
    the coercion of values into data types other than string (all env
    vars are strings be default).

    Args:
        key: string, the name of the env var to look up

    Kwargs:
        default: the default value to return if the env var does not
            exist and required is False
        coerce: a function that is used to coerce the value returned into
            another type - e.g. coerce=lambda x: int(x) would convert a
            string into an integer.
        required: bool, if the env var does not exist and this is True, then
            a RequiredSettingMissing error is raised. NB you cannot set
            required to True and pass in a default value.

    Returns the env var, passed through the coerce function

    """
    assert not (default and required), 'You cannot pass required=True and a default value to get_env.'
    try:
        return coerce(os.environ[key])
    except KeyError:
        if required is True:
            raise RequiredSettingMissing(key)
        else:
            return default


coerce_bool = lambda x: x is not None and x.lower() in ('true', '1', 'y')
coerce_int = lambda x: int(x)
coerce_float = lambda x: float(x)
coerce_decimal = lambda x: decimal.Decimal(x)
coerce_dict = lambda x: json.loads(x)
coerce_datetime = lambda x: parser.parse(x)
coerce_date = lambda x: parser.parse(x).date()

def _get_env(key, *default, **kwargs):
    """
    Unpack default, required and coerce kwargs.

    This is a helper function used to unpack the type-specific get_FOO
    functions' args. Each individual function has one mandatory arg (key),
    and an optional arg (*default) - this is a hack. If a default is not
    passed in, then the env var is assumed to be required.

    This function should never be called directly.

        # 'foo' is a mandatory env var
        >>> get_int('foo')

        # 'foo' is optional
        >>> get_int('foo', 123)

    """
    assert len(default) in (0, 1), 'Too many args supplied.'
    assert 'coerce' in kwargs, "Kwargs must include 'coerce' function arg."
    if len(default) == 0:
        return get_env(key, coerce=kwargs['coerce'], required=True)
    else:
        return get_env(key, default=default[0], coerce=kwargs['coerce'])


def get_bool(key, *default):
    """Return env var cast as boolean."""
    return _get_env(key, coerce=coerce_bool, *default)


def get_int(key, *default):
    """Return env var cast as integer."""
    return _get_env(key, coerce=coerce_int, *default)


def get_float(key, *default):
    """Return env var cast as float."""
    return _get_env(key, coerce=coerce_float, *default)


def get_decimal(key, *default):
    """Return env var cast as Decimal."""
    return _get_env(key, coerce=coerce_decimal, *default)


def get_list(key, separator=' ', *default):
    """Return env var as a list."""
    func = lambda x: x.split(separator)
    return _get_env(key, coerce=func, *default)


def get_dict(key, *default):
    """Return env var as a dict."""
    return _get_env(key, coerce=coerce_dict, *default)


def get_date(key, *default):
    """Return env var as a date."""
    return _get_env(key, coerce=coerce_date, *default)


def get_datetime(key, *default):
    """Return env var as a datetime."""
    return _get_env(key, coerce=coerce_datetime, *default)
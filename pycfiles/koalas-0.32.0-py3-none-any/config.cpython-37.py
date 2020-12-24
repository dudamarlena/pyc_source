# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/config.py
# Compiled at: 2019-10-03 20:45:45
# Size of source mod 2**32: 12211 bytes
"""
Infrastructure of options for Koalas.
"""
import json
from typing import Union, Any, Tuple, Callable, List, Dict
from pyspark._globals import _NoValue, _NoValueType
from databricks.koalas.utils import default_session
__all__ = [
 'get_option', 'set_option', 'reset_option', 'options']

class Option:
    __doc__ = '\n    Option class that defines an option with related properties.\n\n    This class holds all information relevant to the one option. Also,\n    Its instance can validate if the given value is acceptable or not.\n\n    It is currently for internal usage only.\n\n    Parameters\n    ----------\n    key: str, keyword-only argument\n        the option name to use.\n    doc: str, keyword-only argument\n        the documentation for the current option.\n    default: Any, keyword-only argument\n        default value for this option.\n    types: Union[Tuple[type, ...], type], keyword-only argument\n        default is str. It defines the expected types for this option. It is\n        used with `isinstance` to validate the given value to this option.\n    check_func: Tuple[Callable[[Any], bool], str], keyword-only argument\n        default is a function that always returns `True` with a empty string.\n        It defines:\n          - a function to check the given value to this option\n          - the error message to show when this check is failed\n        When new value is set to this option, this function is called to check\n        if the given value is valid.\n\n    Examples\n    --------\n    >>> option = Option(\n    ...     key=\'option.name\',\n    ...     doc="this is a test option",\n    ...     default="default",\n    ...     types=(float, int),\n    ...     check_func=(lambda v: v > 0, "should be a positive float"))\n\n    >>> option.validate(\'abc\')  # doctest: +NORMALIZE_WHITESPACE\n    Traceback (most recent call last):\n      ...\n    ValueError: The value for option \'option.name\' was <class \'str\'>;\n    however, expected types are [(<class \'float\'>, <class \'int\'>)].\n\n    >>> option.validate(-1.1)\n    Traceback (most recent call last):\n      ...\n    ValueError: should be a positive float\n\n    >>> option.validate(1.1)\n    '

    def __init__(self, *, key: str, doc: str, default: Any, types: Union[(Tuple[(type, ...)], type)]=str, check_func: Tuple[(Callable[([Any], bool)], str)]=(
 lambda v: True, '')):
        self.key = key
        self.doc = doc
        self.default = default
        self.types = types
        self.check_func = check_func

    def validate(self, v: Any) -> None:
        """
        Validate the given value and throw an exception with related information such as key.
        """
        if not isinstance(v, self.types):
            raise ValueError("The value for option '%s' was %s; however, expected types are [%s]." % (
             self.key, type(v), str(self.types)))
        if not self.check_func[0](v):
            raise ValueError(self.check_func[1])


_options = [
 Option(key='display.max_rows',
   doc='This sets the maximum number of rows koalas should output when printing out various output. For example, this value determines the number of rows to be shown at the repr() in a dataframe. Set `None` to unlimit the input length. Default is 1000.',
   default=1000,
   types=(
  int, type(None)),
   check_func=(
  lambda v: v is None or v >= 0,
  "'display.max_rows' should be greater than or equal to 0.")),
 Option(key='compute.max_rows',
   doc="'compute.max_rows' sets the limit of the current DataFrame. Set `None` to unlimit the input length. When the limit is set, it is executed by the shortcut by collecting the data into driver side, and then using pandas API. If the limit is unset, the operation is executed by PySpark. Default is 1000.",
   default=1000,
   types=(
  int, type(None)),
   check_func=(
  lambda v: v is None or v >= 0,
  "'compute.max_rows' should be greater than or equal to 0.")),
 Option(key='compute.shortcut_limit',
   doc="'compute.shortcut_limit' sets the limit for a shortcut. It computes specified number of rows and use its schema. When the dataframe length is larger than this limit, Koalas uses PySpark to compute.",
   default=1000,
   types=int,
   check_func=(
  lambda v: v >= 0, "'compute.shortcut_limit' should be greater than or equal to 0.")),
 Option(key='compute.ops_on_diff_frames',
   doc="This determines whether or not to operate between two different dataframes. For example, 'combine_frames' function internally performs a join operation which can be expensive in general. So, if `compute.ops_on_diff_frames` variable is not True, that method throws an exception.",
   default=False,
   types=bool),
 Option(key='compute.default_index_type',
   doc='This sets the default index type: sequence, distributed and distributed-sequence.',
   default='sequence',
   types=str,
   check_func=(
  lambda v: v in ('sequence', 'distributed', 'distributed-sequence'),
  "Index type should be one of 'sequence', 'distributed', 'distributed-sequence'.")),
 Option(key='plotting.max_rows',
   doc="'plotting.max_rows' sets the visual limit on top-n-based plots such as `plot.bar` and `plot.pie`. If it is set to 1000, the first 1000 data points will be used for plotting. Default is 1000.",
   default=1000,
   types=int,
   check_func=(
  lambda v: v is v >= 0,
  "'plotting.max_rows' should be greater than or equal to 0.")),
 Option(key='plotting.sample_ratio',
   doc="'plotting.sample_ratio' sets the proportion of data that will be plotted for sample-based plots such as `plot.line` and `plot.area`. This option defaults to 'plotting.max_rows' option.",
   default=None,
   types=(
  float, type(None)),
   check_func=(
  lambda v: v is None or 1 >= v >= 0,
  "'plotting.sample_ratio' should be 1 >= value >= 0."))]
_options_dict = dict(zip((option.key for option in _options), _options))
_key_format = 'koalas.{}'.format

class OptionError(AttributeError, KeyError):
    pass


def show_options():
    """
    Make a pretty table that can be copied and pasted into public documentation.
    This is currently for an internal purpose.
    """
    import textwrap
    header = [
     'Option', 'Default', 'Description']
    row_format = '{:<31} {:<14} {:<53}'
    print(row_format.format('===============================', '==============', '====================================================='))
    print((row_format.format)(*header))
    print(row_format.format('===============================', '==============', '====================================================='))
    for option in _options:
        doc = textwrap.fill(option.doc, 53)
        formatted = ''.join([line + '\n' + '                                               ' for line in doc.split('\n')]).rstrip()
        print(row_format.format(option.key, repr(option.default), formatted))

    print(row_format.format('===============================', '==============', '====================================================='))


def get_option(key: str, default: Union[(Any, _NoValueType)]=_NoValue) -> Any:
    """
    Retrieves the value of the specified option.

    Parameters
    ----------
    key : str
        The key which should match a single option.
    default : object
        The default value if the option is not set yet. The value should be JSON serializable.

    Returns
    -------
    result : the value of the option

    Raises
    ------
    OptionError : if no such option exists and the default is not provided
    """
    _check_option(key)
    if default is _NoValue:
        default = _options_dict[key].default
    _options_dict[key].validate(default)
    return json.loads(default_session().conf.get((_key_format(key)), default=(json.dumps(default))))


def set_option(key: str, value: Any) -> None:
    """
    Sets the value of the specified option.

    Parameters
    ----------
    key : str
        The key which should match a single option.
    value : object
        New value of option. The value should be JSON serializable.

    Returns
    -------
    None
    """
    _check_option(key)
    _options_dict[key].validate(value)
    default_session().conf.set(_key_format(key), json.dumps(value))


def reset_option(key: str) -> None:
    """
    Reset one option to their default value.

    Pass "all" as argument to reset all options.

    Parameters
    ----------
    key : str
        If specified only option will be reset.

    Returns
    -------
    None
    """
    _check_option(key)
    default_session().conf.unset(_key_format(key))


def _check_option(key: str) -> None:
    if key not in _options_dict:
        raise OptionError("No such option: '{}'. Available options are [{}]".format(key, ', '.join(list(_options_dict.keys()))))


class DictWrapper:
    __doc__ = ' provide attribute-style access to a nested dict'

    def __init__(self, d, prefix=''):
        object.__setattr__(self, 'd', d)
        object.__setattr__(self, 'prefix', prefix)

    def __setattr__(self, key, val):
        prefix = object.__getattribute__(self, 'prefix')
        d = object.__getattribute__(self, 'd')
        if prefix:
            prefix += '.'
        canonical_key = prefix + key
        candidates = [k for k in d.keys() if all((x in k.split('.') for x in canonical_key.split('.')))]
        if len(candidates) == 1:
            if candidates[0] == canonical_key:
                return set_option(canonical_key, val)
        raise OptionError("No such option: '{}'. Available options are [{}]".format(key, ', '.join(list(_options_dict.keys()))))

    def __getattr__(self, key):
        prefix = object.__getattribute__(self, 'prefix')
        d = object.__getattribute__(self, 'd')
        if prefix:
            prefix += '.'
        else:
            canonical_key = prefix + key
            candidates = [k for k in d.keys() if all((x in k.split('.') for x in canonical_key.split('.')))]
            if len(candidates) == 1:
                if candidates[0] == canonical_key:
                    return get_option(canonical_key)
            if len(candidates) == 0:
                raise OptionError("No such option: '{}'. Available options are [{}]".format(key, ', '.join(list(_options_dict.keys()))))
            else:
                return DictWrapper(d, canonical_key)

    def __dir__(self):
        prefix = object.__getattribute__(self, 'prefix')
        d = object.__getattribute__(self, 'd')
        if prefix == '':
            candidates = d.keys()
            offset = 0
        else:
            candidates = [k for k in d.keys() if all((x in k.split('.') for x in prefix.split('.')))]
            offset = len(prefix) + 1
        return [c[offset:] for c in candidates]


options = DictWrapper(_options_dict)
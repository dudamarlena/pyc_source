# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\extra\django\_fields.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 10588 bytes
import re, string
from datetime import timedelta
from decimal import Decimal
from typing import Any, Callable, Dict, Type, TypeVar, Union
import django
import django.db.models as dm
import django.forms as df
from django.core.validators import validate_ipv4_address, validate_ipv6_address, validate_ipv46_address
import hypothesis.strategies as st
from hypothesis.errors import InvalidArgument
from hypothesis.extra.pytz import timezones
from hypothesis.internal.validation import check_type
from hypothesis.provisional import ip4_addr_strings, ip6_addr_strings, urls
from hypothesis.strategies import emails
AnyField = Union[(dm.Field, df.Field)]
F = TypeVar('F', bound=AnyField)
_global_field_lookup = {dm.SmallIntegerField: st.integers(-32768, 32767), 
 dm.IntegerField: st.integers(-2147483648, 2147483647), 
 dm.BigIntegerField: st.integers(-9223372036854775808, 9223372036854775807), 
 dm.PositiveIntegerField: st.integers(0, 2147483647), 
 dm.PositiveSmallIntegerField: st.integers(0, 32767), 
 dm.BinaryField: st.binary(), 
 dm.BooleanField: st.booleans(), 
 dm.DateField: st.dates(), 
 dm.EmailField: emails(), 
 dm.FloatField: st.floats(), 
 dm.NullBooleanField: st.one_of(st.none(), st.booleans()), 
 dm.URLField: urls(), 
 dm.UUIDField: st.uuids(), 
 df.DateField: st.dates(), 
 df.DurationField: st.timedeltas(), 
 df.EmailField: emails(), 
 df.FloatField: st.floats(allow_nan=False, allow_infinity=False), 
 df.IntegerField: st.integers(-2147483648, 2147483647), 
 df.NullBooleanField: st.one_of(st.none(), st.booleans()), 
 df.URLField: urls(), 
 df.UUIDField: st.uuids()}

def register_for(field_type):

    def inner(func):
        _global_field_lookup[field_type] = func
        return func

    return inner


@register_for(dm.DateTimeField)
@register_for(df.DateTimeField)
def _for_datetime(field):
    if getattr(django.conf.settings, 'USE_TZ', False):
        return st.datetimes(timezones=(timezones()))
    return st.datetimes()


def using_sqlite--- This code section failed: ---

 L.  85         0  SETUP_FINALLY        42  'to 42'

 L.  87         2  LOAD_GLOBAL              getattr
                4  LOAD_GLOBAL              django
                6  LOAD_ATTR                conf
                8  LOAD_ATTR                settings
               10  LOAD_STR                 'DATABASES'
               12  BUILD_MAP_0           0 
               14  CALL_FUNCTION_3       3  ''
               16  LOAD_METHOD              get

 L.  88        18  LOAD_STR                 'default'

 L.  88        20  BUILD_MAP_0           0 

 L.  87        22  CALL_METHOD_2         2  ''
               24  LOAD_METHOD              get

 L.  89        26  LOAD_STR                 'ENGINE'

 L.  89        28  LOAD_STR                 ''

 L.  87        30  CALL_METHOD_2         2  ''
               32  LOAD_METHOD              endswith

 L.  90        34  LOAD_STR                 '.sqlite3'

 L.  87        36  CALL_METHOD_1         1  ''

 L.  86        38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY     0  '0'

 L.  92        42  DUP_TOP          
               44  LOAD_GLOBAL              django
               46  LOAD_ATTR                core
               48  LOAD_ATTR                exceptions
               50  LOAD_ATTR                ImproperlyConfigured
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    68  'to 68'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  93        62  POP_EXCEPT       
               64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            54  '54'
               68  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 58


@register_for(dm.TimeField)
def _for_model_time(field):
    if getattr(django.conf.settings, 'USE_TZ', False):
        if not using_sqlite():
            return st.times(timezones=(timezones()))
    return st.times()


@register_for(df.TimeField)
def _for_form_time(field):
    if getattr(django.conf.settings, 'USE_TZ', False):
        return st.times(timezones=(timezones()))
    return st.times()


@register_for(dm.DurationField)
def _for_duration(field):
    if using_sqlite():
        delta = timedelta(microseconds=140737488355327)
        return st.timedeltas(-delta, delta)
    return st.timedeltas()


@register_for(dm.SlugField)
@register_for(df.SlugField)
def _for_slug(field):
    min_size = 1
    if not (getattr(field, 'blank', False) or getattr(field, 'required', True)):
        min_size = 0
    return st.text(alphabet=(string.ascii_letters + string.digits),
      min_size=min_size,
      max_size=(field.max_length))


@register_for(dm.GenericIPAddressField)
def _for_model_ip(field):
    return {'ipv4':ip4_addr_strings(), 
     'ipv6':ip6_addr_strings(), 
     'both':ip4_addr_strings() | ip6_addr_strings()}[field.protocol.lower()]


@register_for(df.GenericIPAddressField)
def _for_form_ip(field):
    if validate_ipv46_address in field.default_validators:
        return ip4_addr_strings() | ip6_addr_strings()
    if validate_ipv4_address in field.default_validators:
        return ip4_addr_strings()
    if validate_ipv6_address in field.default_validators:
        return ip6_addr_strings()
    raise InvalidArgument('No IP version validator on field=%r' % field)


@register_for(dm.DecimalField)
@register_for(df.DecimalField)
def _for_decimal(field):
    bound = Decimal(10 ** field.max_digits - 1) / 10 ** field.decimal_places
    return st.decimals(min_value=(-bound), max_value=bound, places=(field.decimal_places))


@register_for(dm.CharField)
@register_for(dm.TextField)
@register_for(df.CharField)
@register_for(df.RegexField)
def _for_text(field):
    regexes = [re.compile(v.regex, v.flags) if isinstance(v.regex, str) else v.regex for v in field.validators if isinstance(v, django.core.validators.RegexValidator) if not v.inverse_match]
    if regexes:
        return (st.one_of)(*[st.from_regexr for r in regexes])
    min_size = 1
    if not (getattr(field, 'blank', False) or getattr(field, 'required', True)):
        min_size = 0
    strategy = st.text(alphabet=st.characters(blacklist_characters='\x00',
      blacklist_categories=('Cs', )),
      min_size=min_size,
      max_size=(field.max_length))
    if getattr(field, 'required', True):
        strategy = strategy.filter(lambda s: s.strip())
    return strategy


@register_for(df.BooleanField)
def _for_form_boolean(field):
    if field.required:
        return st.justTrue
    return st.booleans()


def register_field_strategy(field_type: Type[AnyField], strategy: st.SearchStrategy) -> None:
    """Add an entry to the global field-to-strategy lookup used by
    :func:`~hypothesis.extra.django.from_field`.

    ``field_type`` must be a subtype of :class:`django.db.models.Field` or
    :class:`django.forms.Field`, which must not already be registered.
    ``strategy`` must be a :class:`~hypothesis.strategies.SearchStrategy`.
    """
    if not issubclass(field_type, (dm.Field, df.Field)):
        raise InvalidArgument('field_type=%r must be a subtype of Field' % (field_type,))
    check_type(st.SearchStrategy, strategy, 'strategy')
    if field_type in _global_field_lookup:
        raise InvalidArgument('field_type=%r already has a registered strategy (%r)' % (
         field_type, _global_field_lookup[field_type]))
    if issubclass(field_type, dm.AutoField):
        raise InvalidArgument('Cannot register a strategy for an AutoField')
    _global_field_lookup[field_type] = strategy


def from_field(field: F) -> st.SearchStrategy[Union[(F, None)]]:
    """Return a strategy for values that fit the given field.

    This function is used by :func:`~hypothesis.extra.django.from_form` and
    :func:`~hypothesis.extra.django.from_model` for any fields that require
    a value, or for which you passed :obj:`hypothesis.infer`.

    It's pretty similar to the core :func:`~hypothesis.strategies.from_type`
    function, with a subtle but important difference: ``from_field`` takes a
    Field *instance*, rather than a Field *subtype*, so that it has access to
    instance attributes such as string length and validators.
    """
    check_type((dm.Field, df.Field), field, 'field')
    if getattr(field, 'choices', False):
        choices = []
        for value, name_or_optgroup in field.choices:
            if isinstance(name_or_optgroup, (list, tuple)):
                choices.extend(key for key, _ in name_or_optgroup)
            else:
                choices.appendvalue
        else:
            if '' in choices:
                choices.remove''
            min_size = 1
            if isinstance(field, (dm.CharField, dm.TextField)) and field.blank:
                choices.insert(0, '')
            else:
                if isinstance(field, df.Field):
                    field.required or choices.insert(0, '')
                    min_size = 0
            strategy = st.sampled_fromchoices
            if isinstance(field, (df.MultipleChoiceField, df.TypedMultipleChoiceField)):
                strategy = st.lists((st.sampled_fromchoices), min_size=min_size)

    else:
        if type(field) not in _global_field_lookup:
            if getattr(field, 'null', False):
                return st.none()
            raise InvalidArgument('Could not infer a strategy for %r', (field,))
        strategy = _global_field_lookup[type(field)]
        if not isinstance(strategy, st.SearchStrategy):
            strategy = strategy(field)
        assert isinstance(strategy, st.SearchStrategy)
        if field.validators:

            def validate--- This code section failed: ---

 L. 277         0  SETUP_FINALLY        18  'to 18'

 L. 278         2  LOAD_DEREF               'field'
                4  LOAD_METHOD              run_validators
                6  LOAD_FAST                'value'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 279        12  POP_BLOCK        
               14  LOAD_CONST               True
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 280        18  DUP_TOP          
               20  LOAD_GLOBAL              django
               22  LOAD_ATTR                core
               24  LOAD_ATTR                exceptions
               26  LOAD_ATTR                ValidationError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 281        38  POP_EXCEPT       
               40  LOAD_CONST               False
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 16

            strategy = strategy.filtervalidate
        if getattr(field, 'null', False):
            return st.none() | strategy
        return strategy
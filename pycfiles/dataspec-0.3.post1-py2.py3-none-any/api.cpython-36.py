# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chrisrink/Projects/dataspec/src/dataspec/api.py
# Compiled at: 2020-05-05 19:56:16
# Size of source mod 2**32: 4493 bytes
import functools
from typing import Mapping, Optional, Tuple, Union
from dataspec.base import Conformer, Spec, SpecPredicate, Tag, ValidationError, all_spec, any_spec, kv_spec, make_spec, merge_spec
from dataspec.factories import blankable_spec, bool_spec, bytes_spec, date_spec, datetime_spec, default_spec, dict_tag_spec, email_spec, every_spec, nilable_spec, num_spec, obj_spec, opt_key, str_spec, time_spec, url_str_spec, uuid_spec
try:
    from dataspec.factories import datetime_str_spec
except ImportError:
    datetime_str_spec = None

try:
    from dataspec.factories import phonenumber_spec
except ImportError:
    phonenumber_spec = None

def _explain(spec: Spec, v) -> Optional[ValidationError]:
    """Return a ValidationError instance containing all of the errors validating ``v``, if
    there were any; return None otherwise."""
    try:
        spec.validate_ex(v)
    except ValidationError as e:
        return e
    else:
        return


def _fdef(argpreds: Tuple[(SpecPredicate, ...)]=(), kwargpreds: Optional[Mapping[(str, SpecPredicate)]]=None, retpred: Optional[SpecPredicate]=None):
    """Wrap a function ``f`` and validate its arguments, keyword arguments, and return
    value with Specs, if any are given."""
    argspecs = s(argpreds) if argpreds else None
    kwargspecs = s(kwargpreds) if kwargpreds else None
    retspec = s(retpred) if retpred else None
    assert [
     argspecs, kwargspecs, retspec].count(None) < 3, 'At least one fdef spec must be given'

    def wrap_f_specs(f):

        @functools.wraps(f)
        def wrapped_f(*args, **kwargs):
            if argspecs is not None:
                argspecs.validate_ex(args)
            else:
                if kwargspecs is not None:
                    kwargspecs.validate_ex(kwargs)
                ret = f(*args, **kwargs)
                if retspec is not None:
                    retspec.validate_ex(ret)
            return ret

        return wrapped_f

    return wrap_f_specs


class SpecAPI:
    __slots__ = ()

    def __call__(self, tag_or_pred: Union[(Tag, SpecPredicate)], *preds: SpecPredicate, conformer: Optional[Conformer]=None) -> Spec:
        return make_spec(tag_or_pred, *preds, **{'conformer': conformer})

    __call__.__doc__ = make_spec.__doc__
    any = staticmethod(any_spec)
    all = staticmethod(all_spec)
    blankable = staticmethod(blankable_spec)
    bool = staticmethod(bool_spec)
    bytes = staticmethod(bytes_spec)
    date = staticmethod(date_spec)
    default = staticmethod(default_spec)
    dict_tag = staticmethod(dict_tag_spec)
    email = staticmethod(email_spec)
    every = staticmethod(every_spec)
    inst = staticmethod(datetime_spec)
    kv = staticmethod(kv_spec)
    merge = staticmethod(merge_spec)
    nilable = staticmethod(nilable_spec)
    num = staticmethod(num_spec)
    obj = staticmethod(obj_spec)
    str = staticmethod(str_spec)
    time = staticmethod(time_spec)
    url = staticmethod(url_str_spec)
    uuid = staticmethod(uuid_spec)
    is_any = every_spec('is_any')
    is_bool = bool_spec('is_bool')
    is_bytes = bytes_spec('is_bytes')
    is_date = date_spec('is_date')
    is_email = email_spec('is_email')
    is_false = bool_spec('is_false', allowed_values={False})
    is_float = num_spec('is_float', type_=float)
    is_inst = datetime_spec('is_inst')
    is_int = num_spec('is_int', type_=int)
    is_num = num_spec('is_num')
    is_str = str_spec('is_str')
    is_time = time_spec('is_str')
    is_true = bool_spec('is_true', allowed_values={True})
    is_uuid = uuid_spec('is_true')
    explain = staticmethod(_explain)
    fdef = staticmethod(_fdef)
    opt = staticmethod(opt_key)
    if datetime_str_spec is not None:
        inst_str = staticmethod(datetime_str_spec)
    if phonenumber_spec is not None:
        phone = staticmethod(phonenumber_spec)


s = SpecAPI()
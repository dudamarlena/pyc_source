# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyDots\__init__.py
# Compiled at: 2017-01-16 16:05:05
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __builtin__ import zip as _builtin_zip
from collections import Mapping
from types import GeneratorType, NoneType, ModuleType
SELF_PATH = b'.'
ROOT_PATH = [SELF_PATH]
_get = object.__getattribute__

def inverse(d):
    """
    reverse the k:v pairs
    """
    output = {}
    for k, v in unwrap(d).iteritems():
        output[v] = output.get(v, [])
        output[v].append(k)

    return output


def coalesce(*args):
    for a in args:
        if a != None:
            return wrap(a)

    return Null


def zip(keys, values):
    """
    CONVERT LIST OF KEY/VALUE PAIRS TO A DICT
    PLEASE `import dot`, AND CALL `dot.zip()`
    """
    output = Data()
    for i, k in enumerate(keys):
        if i >= len(values):
            break
        output[k] = values[i]

    return output


def literal_field(field):
    """
    RETURN SAME WITH DOTS (`.`) ESCAPED
    """
    try:
        return field.replace(b'.', b'\\.')
    except Exception as e:
        from MoLogs import Log
        Log.error(b'bad literal', e)


def split_field(field):
    """
    RETURN field AS ARRAY OF DOT-SEPARATED FIELDS
    """
    if field == b'.' or field == None:
        return []
    if field.find(b'.') >= 0:
        field = field.replace(b'\\.', b'\x07')
        return [ k.replace(b'\x07', b'.') for k in field.split(b'.') ]
    else:
        return [
         field]
        return


def join_field(field):
    """
    RETURN field SEQUENCE AS STRING
    """
    potent = [ f for f in field if f != b'.' ]
    if not potent:
        return b'.'
    return (b'.').join([ f.replace(b'.', b'\\.') for f in potent ])


def concat_field(prefix, suffix):
    return join_field(split_field(prefix) + split_field(suffix))


def startswith_field(field, prefix):
    """
    RETURN True IF field PATH STRING STARTS WITH prefix PATH STRING
    """
    if prefix == b'.':
        return True
    if field.startswith(prefix):
        if len(field) == len(prefix) or field[len(prefix)] == b'.':
            return True
    return False


def relative_field(field, parent):
    """
    RETURN field PATH WITH RESPECT TO parent
    """
    if parent == b'.':
        return field
    else:
        field_path = split_field(field)
        parent_path = split_field(parent)
        common = 0
        for f, p in _builtin_zip(field_path, parent_path):
            if f != p:
                break
            common += 1

        if len(parent_path) == common:
            return join_field(field_path[common:])
        dots = b'.' * (len(parent_path) - common)
        return dots + b'.' + join_field(field_path[common:])


def hash_value(v):
    if isinstance(v, (set, tuple, list)):
        return hash(tuple(hash_value(vv) for vv in v))
    else:
        if not isinstance(v, Mapping):
            return hash(v)
        return hash(tuple(sorted(hash_value(vv) for vv in v.values())))


def _setdefault(obj, key, value):
    """
    DO NOT USE __dict__.setdefault(obj, key, value), IT DOES NOT CHECK FOR obj[key] == None
    """
    v = obj.get(key)
    if v == None:
        obj[key] = value
        return value
    else:
        return v


def set_default(*params):
    """
    INPUT dicts IN PRIORITY ORDER
    UPDATES FIRST dict WITH THE MERGE RESULT, WHERE MERGE RESULT IS DEFINED AS:
    FOR EACH LEAF, RETURN THE HIGHEST PRIORITY LEAF VALUE
    """
    p0 = params[0]
    agg = p0 if p0 or isinstance(p0, Mapping) else {}
    for p in params[1:]:
        p = unwrap(p)
        if p is None:
            continue
        _all_default(agg, p, seen={})

    return wrap(agg)


def _all_default(d, default, seen=None):
    """
    ANY VALUE NOT SET WILL BE SET BY THE default
    THIS IS RECURSIVE
    """
    if default is None:
        return
    else:
        if isinstance(default, Data):
            default = object.__getattribute__(default, b'_dict')
        for k, default_value in default.items():
            default_value = unwrap(default_value)
            existing_value = _get_attr(d, [k])
            if existing_value == None:
                if default_value != None:
                    if isinstance(default_value, Mapping):
                        df = seen.get(id(default_value))
                        if df is not None:
                            _set_attr(d, [k], df)
                        else:
                            copy_dict = {}
                            seen[id(default_value)] = copy_dict
                            _set_attr(d, [k], copy_dict)
                            _all_default(copy_dict, default_value, seen)
                    else:
                        try:
                            _set_attr(d, [k], default_value)
                        except Exception as e:
                            if PATH_NOT_FOUND not in e:
                                from MoLogs import Log
                                Log.error(b'Can not set attribute {{name}}', name=k, cause=e)

            elif isinstance(existing_value, list) or isinstance(default_value, list):
                _set_attr(d, [k], listwrap(existing_value) + listwrap(default_value))
            elif (hasattr(existing_value, b'__setattr__') or isinstance(existing_value, Mapping)) and isinstance(default_value, Mapping):
                df = seen.get(id(default_value))
                if df is not None:
                    _set_attr(d, [k], df)
                else:
                    seen[id(default_value)] = existing_value
                    _all_default(existing_value, default_value, seen)

        return


def _getdefault(obj, key):
    """
    obj MUST BE A DICT
    key IS EXPECTED TO BE LITERAL (NO ESCAPING)
    TRY BOTH ATTRIBUTE AND ITEM ACCESS, OR RETURN Null
    """
    try:
        return obj[key]
    except Exception as f:
        pass

    try:
        return getattr(obj, key)
    except Exception as f:
        pass

    try:
        if float(key) == round(float(key), 0):
            return obj[int(key)]
    except Exception as f:
        pass

    return NullType(obj, key)


PATH_NOT_FOUND = b'Path not found'
AMBIGUOUS_PATH_FOUND = b'Path is ambiguous'

def set_attr(obj, path, value):
    """
    SAME AS object.__setattr__(), BUT USES DOT-DELIMITED path
    RETURN OLD VALUE
    """
    try:
        return _set_attr(obj, split_field(path), value)
    except Exception as e:
        from MoLogs import Log
        if PATH_NOT_FOUND in e:
            Log.warning(PATH_NOT_FOUND + b': {{path}}', path=path)
        else:
            Log.error(b'Problem setting value', e)


def get_attr(obj, path):
    """
    SAME AS object.__getattr__(), BUT USES DOT-DELIMITED path
    """
    try:
        return _get_attr(obj, split_field(path))
    except Exception as e:
        from MoLogs import Log
        if PATH_NOT_FOUND in e:
            Log.error(PATH_NOT_FOUND + b': {{path}}', path=path, cause=e)
        else:
            Log.error(b'Problem setting value', e)


def _get_attr(obj, path):
    if not path:
        return obj
    else:
        attr_name = path[0]
        if isinstance(obj, ModuleType):
            if attr_name in obj.__dict__:
                return _get_attr(obj.__dict__[attr_name], path[1:])
            if attr_name in dir(obj):
                return _get_attr(obj[attr_name], path[1:])
            from pyLibrary.env.files import File
            possible_error = None
            if File.new_instance(File(obj.__file__).parent, attr_name).set_extension(b'py').exists:
                try:
                    if len(path) == 1:
                        output = __import__(obj.__name__ + b'.' + attr_name, globals(), locals(), [path[0]], 0)
                        return output
                    else:
                        output = __import__(obj.__name__ + b'.' + attr_name, globals(), locals(), [path[1]], 0)
                        return _get_attr(output, path[1:])

                except Exception as e:
                    from MoLogs.exceptions import Except
                    possible_error = Except.wrap(e)

            matched_attr_name = lower_match(attr_name, dir(obj))
            if not matched_attr_name:
                from MoLogs import Log
                Log.warning(PATH_NOT_FOUND + b'({{name|quote}}) Returning None.', name=attr_name, cause=possible_error)
            elif len(matched_attr_name) > 1:
                from MoLogs import Log
                Log.error(AMBIGUOUS_PATH_FOUND + b' {{paths}}', paths=attr_name)
            else:
                return _get_attr(obj[matched_attr_name[0]], path[1:])
        try:
            obj = obj[int(attr_name)]
            return _get_attr(obj, path[1:])
        except Exception:
            pass

        try:
            obj = getattr(obj, attr_name)
            return _get_attr(obj, path[1:])
        except Exception:
            pass

        try:
            obj = obj[attr_name]
            return _get_attr(obj, path[1:])
        except Exception as f:
            return

        return


def _set_attr(obj, path, value):
    obj = _get_attr(obj, path[:-1])
    if obj is None:
        from MoLogs import Log
        Log.error(PATH_NOT_FOUND)
    attr_name = path[(-1)]
    try:
        old_value = _get_attr(obj, [attr_name])
        if old_value == None:
            old_value = None
            new_value = value
        else:
            new_value = old_value.__class__(value)
    except Exception as e:
        old_value = None
        new_value = value

    try:
        setattr(obj, attr_name, new_value)
        return old_value
    except Exception as e:
        try:
            obj[attr_name] = new_value
            return old_value
        except Exception as f:
            from MoLogs import Log
            Log.error(PATH_NOT_FOUND)

    return


def lower_match(value, candidates):
    return [ v for v in candidates if v.lower() == value.lower() ]


def wrap(v):
    type_ = _get(v, b'__class__')
    if type_ is dict:
        m = Data(v)
        return m
    else:
        if type_ is NoneType:
            return Null
        if type_ is list:
            return FlatList(v)
        if type_ is GeneratorType:
            return (wrap(vv) for vv in v)
        return v


def wrap_leaves(value):
    """
    dict WITH DOTS IN KEYS IS INTERPRETED AS A PATH
    """
    return wrap(_wrap_leaves(value))


def _wrap_leaves(value):
    if value == None:
        return
    else:
        if isinstance(value, (basestring, int, float)):
            return value
        if isinstance(value, Mapping):
            if isinstance(value, Data):
                value = unwrap(value)
            output = {}
            for key, value in value.iteritems():
                value = _wrap_leaves(value)
                if key == b'':
                    from MoLogs import Log
                    Log.error(b'key is empty string.  Probably a bad idea')
                if isinstance(key, str):
                    key = key.decode(b'utf8')
                d = output
                if key.find(b'.') == -1:
                    if value is None:
                        d.pop(key, None)
                    else:
                        d[key] = value
                else:
                    seq = split_field(key)
                    for k in seq[:-1]:
                        e = d.get(k, None)
                        if e is None:
                            d[k] = {}
                            e = d[k]
                        d = e

                    if value == None:
                        d.pop(seq[(-1)], None)
                    else:
                        d[seq[(-1)]] = value

            return output
        if hasattr(value, b'__iter__'):
            output = []
            for v in value:
                v = wrap_leaves(v)
                output.append(v)

            return output
        return value


def unwrap(v):
    _type = _get(v, b'__class__')
    if _type is Data:
        d = _get(v, b'_dict')
        return d
    else:
        if _type is FlatList:
            return v.list
        else:
            if _type is NullType:
                return
            if _type is GeneratorType:
                return (unwrap(vv) for vv in v)
            return v

        return


def listwrap(value):
    """
    PERFORMS THE FOLLOWING TRANSLATION
    None -> []
    value -> [value]
    [...] -> [...]  (unchanged list)

    ##MOTIVATION##
    OFTEN IT IS NICE TO ALLOW FUNCTION PARAMETERS TO BE ASSIGNED A VALUE,
    OR A list-OF-VALUES, OR NULL.  CHECKING FOR WHICH THE CALLER USED IS
    TEDIOUS.  INSTEAD WE CAST FROM THOSE THREE CASES TO THE SINGLE CASE
    OF A LIST

    # BEFORE
    def do_it(a):
        if a is None:
            return
        if not isinstance(a, list):
            a=[a]
        for x in a:
            # do something

    # AFTER
    def do_it(a):
        for x in listwrap(a):
            # do something

    """
    if value == None:
        return FlatList()
    else:
        if isinstance(value, list):
            return wrap(value)
        else:
            if isinstance(value, set):
                return wrap(list(value))
            return wrap([unwrap(value)])

        return


def unwraplist(v):
    """
    LISTS WITH ZERO AND ONE element MAP TO None AND element RESPECTIVELY
    """
    if isinstance(v, list):
        if len(v) == 0:
            return
        else:
            if len(v) == 1:
                return unwrap(v[0])
            return unwrap(v)

    else:
        return unwrap(v)
    return


def tuplewrap(value):
    """
    INTENDED TO TURN lists INTO tuples FOR USE AS KEYS
    """
    if isinstance(value, (list, set, tuple, GeneratorType)):
        return tuple((tuplewrap(v) if isinstance(v, (list, tuple, GeneratorType)) else v) for v in value)
    return (
     unwrap(value),)


from pyDots.nones import Null, NullType
from pyDots.datas import Data
from pyDots.lists import FlatList
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/util/eq.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 1101 bytes
from numpy import ndarray, bool_

def eq(a, b):
    """ The great missing equivalence function: Guaranteed evaluation
    to a single bool value.
    """
    if a is b:
        return True
    if a is None or b is None:
        if a is None and b is None:
            return True
        else:
            return False
    try:
        e = a == b
    except ValueError:
        return False
    except AttributeError:
        return False
    except Exception:
        print('a:', str(type(a)), str(a))
        print('b:', str(type(b)), str(b))
        raise

    t = type(e)
    if t is bool:
        return e
    if t is bool_:
        return bool(e)
    if isinstance(e, ndarray):
        try:
            if a.shape != b.shape:
                return False
        except Exception:
            return False

        if hasattr(e, 'implements') and e.implements('MetaArray'):
            return e.asarray().all()
        else:
            return e.all()
    else:
        raise Exception('== operator returned type %s' % str(type(e)))
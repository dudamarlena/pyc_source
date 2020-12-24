# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/util/eq.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 1101 bytes
from numpy import ndarray, bool_

def eq(a, b):
    """ The great missing equivalence function: Guaranteed evaluation
    to a single bool value.
    """
    if a is b:
        return True
        if a is None or b is None:
            if a is None:
                if b is None:
                    return True
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
            else:
                if hasattr(e, 'implements'):
                    if e.implements('MetaArray'):
                        return e.asarray().all()
                return e.all()
    else:
        raise Exception('== operator returned type %s' % str(type(e)))
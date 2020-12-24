# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/eq.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1082 bytes
from numpy import ndarray, bool_
from ..metaarray import MetaArray

def eq(a, b):
    """The great missing equivalence function: Guaranteed evaluation to a single bool value."""
    if a is b:
        return True
        try:
            e = a == b
        except ValueError:
            return False
        except AttributeError:
            return False
        except:
            print('a:', str(type(a)), str(a))
            print('b:', str(type(b)), str(b))
            raise

        t = type(e)
        if t is bool:
            return e
            if t is bool_:
                return bool(e)
            if not isinstance(e, ndarray):
                if not hasattr(e, 'implements') or e.implements('MetaArray'):
                    try:
                        if a.shape != b.shape:
                            return False
                    except:
                        return False

        elif hasattr(e, 'implements') and e.implements('MetaArray'):
            return e.asarray().all()
        return e.all()
    else:
        raise Exception('== operator returned type %s' % str(type(e)))
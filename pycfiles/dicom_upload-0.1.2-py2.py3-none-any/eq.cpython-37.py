# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
                    if hasattr(e, 'implements'):
                        if e.implements('MetaArray'):
                            return e.asarray().all()
                    return e.all()

    else:
        raise Exception('== operator returned type %s' % str(type(e)))
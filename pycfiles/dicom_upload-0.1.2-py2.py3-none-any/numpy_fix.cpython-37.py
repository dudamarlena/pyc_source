# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/numpy_fix.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 860 bytes
try:
    import numpy as np
    if not hasattr(np, 'concatenate_orig'):
        np.concatenate_orig = np.concatenate

    def concatenate(vals, *args, **kwds):
        """Wrapper around numpy.concatenate (see pyqtgraph/numpy_fix.py)"""
        dtypes = [getattr(v, 'dtype', None) for v in vals]
        names = [getattr(dt, 'names', None) for dt in dtypes]
        if len(dtypes) < 2 or all([n is None for n in names]):
            return (np.concatenate_orig)(vals, *args, **kwds)
        if any([dt != dtypes[0] for dt in dtypes[1:]]):
            raise TypeError('Cannot concatenate structured arrays of different dtype.')
        return (np.concatenate_orig)(vals, *args, **kwds)


    np.concatenate = concatenate
except ImportError:
    pass
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/utils/_safe_eval_float.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 1023 bytes
from typing import Union as _Union
__all__ = [
 'safe_eval_float']

def safe_eval_float(s: _Union[(float, int, str)]) -> float:
    """Convert 's' to a float. This supports normal floats,
       but also simple maths expressions like 1/1.2,
       plus anything that ends with a "%" is recognised
       as a percentage

       Examples
       --------

       safe_eval_float(0.3)         -> 0.3
       safe_eval_float("5%")        -> 0.05
       safe_eval_float("1/4")       -> 0.25
       safe_eval_float("(30+100)%)  -> 1.3
    """
    try:
        return float(s)
    except Exception:
        pass

    try:
        return float(eval(s, {'__builtins__': None}, {}))
    except Exception:
        pass

    if isinstance(s, str):
        s = s.strip()
        if s.endswith('%'):
            try:
                return safe_eval_float(s[0:-1]) / 100.0
            except Exception:
                pass

    raise ValueError(f"Cannot interpret '{s}' as a float")
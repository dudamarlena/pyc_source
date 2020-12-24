# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\django\core\utils.py
# Compiled at: 2018-02-12 22:15:16
# Size of source mod 2**32: 1333 bytes
import importlib.util, sys

def _import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod


def _reverse(seq):
    SeqType = type(seq)
    emptySeq = SeqType()
    if seq == emptySeq:
        return emptySeq
    restrev = _reverse(seq[1:])
    first = seq[0:1]
    result = restrev + first
    return result


def load_module(name):
    if name in sys.modules:
        return sys.modules[name]
    arr_name = name.split('.')
    len_name = len(arr_name)
    spec = None
    for i in range(0, len_name):
        lidx = len_name - i
        try:
            spec = importlib.util.find_spec('.'.join(arr_name[0:lidx]))
            if spec is not None:
                pass
            break
        except Exception:
            pass

    if spec is None:
        return
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for i in range(lidx, len_name):
        if not hasattr(module, arr_name[i]):
            return
        module = getattr(module, arr_name[i])

    return module
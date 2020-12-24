# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/impl/utils/split.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 2093 bytes
import pickle
SIZE_LIMIT = 268435456

def split_put(k, v, use_serialize, put_call_back_func):
    if use_serialize is False:
        raise NotImplementedError('not support put large value without serialization yet!')
    v_bytes = pickle.dumps(v)
    num_bytes = len(v_bytes)
    num_splits = (num_bytes - 1) // SIZE_LIMIT + 1
    view = memoryview(v_bytes)
    put_call_back_func.put(k, num_splits, use_serialize=True)
    for i in range(num_splits):
        if use_serialize is None:
            put_call_back_func.put(k=(pickle.dumps(f"{k}__frag_{i}")), v=(view[SIZE_LIMIT * i:SIZE_LIMIT * (i + 1)]))
        else:
            put_call_back_func.put(k=(pickle.dumps(f"{k}__frag_{i}")), v=(view[SIZE_LIMIT * i:SIZE_LIMIT * (i + 1)]),
              use_serialize=False)

    return True


def split_get(k, use_serialize, get_call_back_func):
    if use_serialize is False:
        raise NotImplementedError('not support get large value without serialization yet!')
    k_bytes = pickle.dumps(k)
    num_split = pickle.loads(k_bytes)
    splits = []
    for i in range(num_split):
        if use_serialize is None:
            splits.append(get_call_back_func(k=(pickle.dumps(f"{k}__frag_{i}"))))
        else:
            splits.append(get_call_back_func(k=(pickle.dumps(f"{k}__frag_{i}")), use_serialize=False))

    v_bytes = (bytes.join)(*splits)
    v = pickle.loads(v_bytes)
    return v
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/dlblocks/pyutils.py
# Compiled at: 2018-12-11 12:52:10
import numpy as np, json
from tqdm import tqdm
import os

def set_gpu(gpu_id):
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)


def loadJson(fname):
    return json.loads(open(fname).read())


def saveJson(fname, data):
    open(fname, 'wb').write(json.dumps(data))


def mapArrays(data, func, *args, **kwargs):
    L = None
    for d in tqdm(data):
        mapped = func(d, *args, **kwargs)
        if L is None:
            if type(mapped) is list:
                L = [ [] for _ in len(mapped) ]
            elif type(mapped) is tuple:
                L = tuple([ [] for _ in len(mapped) ])
            elif type(mapped) is dict:
                L = {key:[] for key in mapped.keys()}
            else:
                L = []
        if type(mapped) is list or type(mapped) is tuple:
            if any(map(lambda x: x is None, mapped)):
                continue
            for i, m in enumerate(mapped):
                L[i].append(m)

        elif type(mapped) is dict:
            for key in mapped.keys():
                L[key].append(mapped[key])

        else:
            L.append(mapped)

    if type(L) is dict:
        for k in L.keys():
            L[k] = np.array(L[k])

    else:
        L = map(np.array, L)
    return L


def oneHotVec(classId, nClasses):
    v = np.zeros(nClasses)
    v[classId] = 1
    return v


def selectKeys(items, keys):
    if type(keys) is list or type(keys) is tuple:
        LL = []
        for key in keys:
            l = [ x[key] for x in items ]
            LL.append(l)

        if type(keys) is tuple:
            LL = tuple(LL)
        return LL
    key = keys
    return [ x[key] for x in items ]


def padList(inp, maxLen, el=0, side='right'):
    if side == 'right':
        inp = inp[:maxLen]
    else:
        inp = inp[-1 * maxLen:]
    if len(inp) < maxLen:
        if side == 'right':
            inp = inp + [el] * (maxLen - len(inp))
        else:
            inp = [
             el] * (maxLen - len(inp)) + inp
    return inp


def int64Arr(d):
    return np.array(d).astype('int64')


def floatArr(d):
    return np.array(d).astype('int64')


def env_arg(key, default=None, type=str):
    key = str(key)
    if type is bool:
        type = lambda x: bool(int(x))
    if key in os.environ:
        r = type(os.environ[key])
        print key, '->', r
        return r
    else:
        if default is not None:
            r = default
            print key, '->', r, '(default)'
            return r
        raise Exception(key + ' Not found')
        return


def makeGenerator(data):
    for d in data:
        yield d


def mapGenerator(fn, g):
    for d in g:
        yield fn(d)


def loadJsonAppend(fname):
    import ijson, subprocess
    read_process = subprocess.Popen('echo "[";  cat "%s" | head -c -2   ; echo "]" ' % fname, shell=True, stdout=subprocess.PIPE)
    FF = ijson.items(read_process.stdout, 'item')
    for item in FF:
        yield item
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/utils/_logging.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 791 bytes
import numpy as np, json

class Encoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            if type(obj) in [np.int32, np.int64]:
                return int(obj)
            if type(obj) in [np.float32, np.float64]:
                return float(obj)
            return json.JSONEncoder.default(self, obj)


class JsonMessage(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        s = json.dumps((self.kwargs), cls=Encoder)
        return '>>> %s' % s


def test_ndarray():
    t = np.array([1, 2])
    jm = JsonMessage(t=t)
    print(jm)


if __name__ == '__main__':
    test_ndarray()
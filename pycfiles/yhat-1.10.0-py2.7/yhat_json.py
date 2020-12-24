# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yhat/yhat_json.py
# Compiled at: 2017-04-26 17:15:42
import json
try:
    import numpy as np
except ImportError as e:
    np = None

class NumpyAwareJSONEncoder(json.JSONEncoder):
    """
    NumpyAwareJSONEncoder makes numpy arrays JSON serializeable. This is important
    because most mathematical libraries return numpy arrays instead of python lists.

    If there was a new numpy data type that you wanted to make JSON serializeable,
    all you'd need to do is edit the `default` method below. This could also be
    modified in the future to serialize non-numpy specific data types (though you'd
    prboably want to change the name of the class).
    """

    def __init__(self, nan_str='null', **kwargs):
        super(NumpyAwareJSONEncoder, self).__init__(**kwargs)
        self.nan_str = nan_str
        self.allow_nan = True

    def default(self, obj):
        if np and isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

    def iterencode(self, o, _one_shot=False):
        """
        Encode the given object and yield each string representation as
        available.

        For example:
            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)
        """
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = json.encoder.encode_basestring_ascii
        else:
            _encoder = json.encoder.encode_basestring

        def floatstr(o, allow_nan=self.allow_nan, _repr=repr, _inf=json.encoder.INFINITY, _neginf=-json.encoder.INFINITY, nan_str=self.nan_str):
            if o != o:
                text = nan_str
            elif o == _inf:
                text = 'Infinity'
            elif o == _neginf:
                text = '-Infinity'
            else:
                return _repr(o)
            if not allow_nan:
                raise ValueError('Out of range float values are not JSON compliant: ' + repr(o))
            return text

        _iterencode = json.encoder._make_iterencode(markers, self.default, _encoder, self.indent, floatstr, self.key_separator, self.item_separator, self.sort_keys, self.skipkeys, _one_shot)
        return _iterencode(o, 0)


def json_dumps(data, **kwargs):
    """
    Uses json.dumps to serialize data into JSON. In addition to the standard
    json.dumps function, we're also using the NumpyAwareJSONEncoder to handle
    numpy arrays and the `ignore_nan` parameter by default to handle np.nan values.
    """
    return json.dumps(data, cls=NumpyAwareJSONEncoder, allow_nan=False)
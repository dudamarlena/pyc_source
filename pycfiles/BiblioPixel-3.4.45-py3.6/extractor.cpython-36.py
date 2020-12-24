# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/extractor.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 3251 bytes
import collections

class Extractor:
    __doc__ = '\n    Extractor is a class that extracts and normalizes values from\n    incoming message dictionaries into ordered dictionaries based on the\n    `type` key of each message.\n    '

    def __init__(self, omit=None, normalizers=None, keys_by_type=None, accept=None, reject=None, auto_omit=True):
        """
        Arguments

        omit -- A list of keys that will not be extracted.

        normalizers -- Some keys also need to be "normalized" -
            scaled and offset so they are between 0 and 1, or -1 and 1.
            The `normalizers` table maps key names to a function that
            normalizes the value of that key.

        keys_by_type -- `keys_by_type` is a dictionary from the `type` in an
            incoming message to a list of message keys to be extracted

        accept -- maps keys to a value or a list of values that are
            accepted for that key.  A message has to match *all* entries in
            `accept` to be accepted.

        reject -- map key to a value or a list of values that are not
            accepted for that key.  A message is rejected if it matches *any*
            entry in the reject map.

        auto_omit -- if True, omit all keys in `accept` that only have one
            possible value.

            auto_omit=True, the default, is probably more useful: if you
            request data for channel=1, type=note_on then you probably don't
            want to see channel=1, type=note_on with each message.
        """

        def to_set(x):
            if x is None:
                return set()
            else:
                if isinstance(x, (list, tuple)):
                    return set(x)
                return set([x])

        def make_match(m):
            return m and {k:to_set(v) for k, v in m.items()}

        self.accept, self.reject = make_match(accept), make_match(reject)
        self.omit = to_set(omit)
        if auto_omit:
            if self.accept:
                self.omit.update(k for k, v in self.accept.items() if len(v) == 1)
        else:
            self.normalizers = normalizers or {}
            if keys_by_type is None:
                self.keys_by_type = None
            else:
                self.keys_by_type = {}
                for k, v in keys_by_type.items():
                    if isinstance(v, str):
                        v = [
                         v]
                    self.keys_by_type[k] = tuple(i for i in v if i not in self.omit)

    def extract(self, msg):
        """Yield an ordered dictionary if msg['type'] is in keys_by_type."""

        def normal(key):
            v = msg.get(key)
            if v is None:
                return v
            else:
                normalizer = self.normalizers.get(key, lambda x: x)
                return normalizer(v)

        def odict(keys):
            return collections.OrderedDict((k, normal(k)) for k in keys)

        def match(m):
            if m:
                return (msg.get(k) in v for k, v in m.items())
            else:
                return ()

        accept = all(match(self.accept))
        reject = any(match(self.reject))
        if reject or not accept:
            keys = ()
        else:
            if self.keys_by_type is None:
                keys = [k for k in msg.keys() if k not in self.omit]
            else:
                keys = self.keys_by_type.get(msg.get('type'))
        return odict(keys)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/profile.py
# Compiled at: 2018-10-15 03:11:35
# Size of source mod 2**32: 2066 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging, json, collections

class DotDict(dict):

    def __init__(self, *args):
        """ This class simplifies the use of "."-separated
            keys when defining a nested dictionary:::

                >>> from dpaycli.profile import Profile
                >>> keys = ['profile.url', 'profile.img']
                >>> values = ["http:", "foobar"]
                >>> p = Profile(keys, values)
                >>> print(p["profile"]["url"])
                http:

        """
        if len(args) == 2:
            for i, item in enumerate(args[0]):
                t = self
                parts = item.split('.')
                for j, part in enumerate(parts):
                    if j < len(parts) - 1:
                        t = t.setdefault(part, {})
                    else:
                        t[part] = args[1][i]

        else:
            if len(args) == 1:
                if isinstance(args[0], dict):
                    for k, v in args[0].items():
                        self[k] = v

        if len(args) == 1:
            if isinstance(args[0], str):
                for k, v in json.loads(args[0]).items():
                    self[k] = v


class Profile(DotDict):
    __doc__ = " This class is a template to model a user's on-chain\n        profile according to\n\n            * https://github.com/adcpm/dpayscript\n    "

    def __init__(self, *args, **kwargs):
        (super(Profile, self).__init__)(*args, **kwargs)

    def __str__(self):
        return json.dumps(self)

    def update(self, u):
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                self.setdefault(k, {}).update(v)
            else:
                self[k] = u[k]

    def remove(self, key):
        parts = key.split('.')
        if len(parts) > 1:
            self[parts[0]].pop('.'.join(parts[1:]))
        else:
            super(Profile, self).pop(parts[0], None)
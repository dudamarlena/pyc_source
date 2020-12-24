# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/mturk/layoutparam.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2045 bytes


class LayoutParameters(object):

    def __init__(self, layoutParameters=None):
        if layoutParameters is None:
            layoutParameters = []
        self.layoutParameters = layoutParameters

    def add(self, req):
        self.layoutParameters.append(req)

    def get_as_params(self):
        params = {}
        assert len(self.layoutParameters) <= 25
        for n, layoutParameter in enumerate(self.layoutParameters):
            kv = layoutParameter.get_as_params()
            for key in kv:
                params['HITLayoutParameter.%s.%s' % (n + 1, key)] = kv[key]

        return params


class LayoutParameter(object):
    __doc__ = '\n    Representation of a single HIT layout parameter\n    '

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_as_params(self):
        params = {'Name': self.name, 
         'Value': self.value}
        return params
# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """LayoutParameter"""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_as_params(self):
        params = {'Name': self.name, 
         'Value': self.value}
        return params
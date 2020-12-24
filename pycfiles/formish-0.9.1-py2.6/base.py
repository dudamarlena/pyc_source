# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/formish/tests/unittests/base.py
# Compiled at: 2010-01-04 05:35:21
import unittest
from webob.multidict import MultiDict

class Request(object):
    headers = {'content-type': 'text/html'}

    def __init__(self, form_name='form', POST=None):
        if POST is None:
            POST = {}
        self.POST = MultiDict(POST)
        self.POST['__formish_form__'] = form_name
        self.GET = self.POST
        self.method = 'POST'
        return


class TestCase(unittest.TestCase):
    Request = Request
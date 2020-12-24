# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\underverse\tests\kv_test.py
# Compiled at: 2012-02-20 13:00:57
from underverse import Underverse, NecRow
from underverse.model import Document as D
from test_data_gen import Person
import unittest, os

class KeyValueTestCase(unittest.TestCase):

    def setUp(self):
        self.uv = Underverse()

    def tearDown(self):
        self.uv.close()

    def test_add_key(self):
        self.test = self.uv.test
        self.test.put('key', 5)
        test = True
        try:
            self.test.get('key')
        except Exception as e:
            test = False

        self.assertTrue(test)

    def test_add_key_fail(self):
        self.test = self.uv.test
        test = True
        try:
            self.test.get('key2')
        except Exception as e:
            test = False

        self.assertFalse(test)

    def test_add_key_obj(self):
        self.test = self.uv.test

        class kv(object):
            """docstring for kv"""

            def __init__(self, arg):
                super(kv, self).__init__()
                self.arg = arg

        self.test.put('key', kv(5))
        test = True
        try:
            k = self.test.get('key')
        except Exception as e:
            test = False

        self.assertTrue(test)

    def test_add_key_list(self):
        self.test = self.uv.test
        self.test.put('key', range(5))
        test = True
        try:
            k = self.test.get('key')
            if type(k.value) != list:
                test = False
        except Exception as e:
            test = False

        self.assertTrue(test)

    def test_add_key_dict(self):
        self.test = self.uv.test
        self.test.put('key', {'a': 1, 'b': range(5)})
        test = True
        try:
            k = self.test.get('key')
            if type(k.value) != dict:
                test = False
            if type(k.b) != list:
                test = False
        except Exception as e:
            test = False

        self.assertTrue(test)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KeyValueTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    exit()
    uv = Underverse()
    options = uv.options
    times = uv.times
    from datetime import datetime
    times.add({'time': datetime.now()})
    for t in times:
        print t

    exit()
    options.put('DEVMODES', {'TEST': 0, 'DEV': 1, 'PROD': 2})
    DEVMODES = options.get('DEVMODES')
    print DEVMODES.PROD
    DEVMODES = options.get('DEVMODES')
    DEVMODES = options.get('DEVMODES.DEV')
    print DEVMODES
    options.add({'TEST': 0, 'DEV': 1, 'PROD': 2})
    for o in options:
        print o.TEST

    test = uv.test

    class User(NecRow):

        def __init__(self, name, fullname, password):
            self.name = name
            self.fullname = fullname
            self.password = password


    class Comment(object):
        """docstring for Comment"""

        def __init__(self, text):
            super(Comment, self).__init__()
            self.text = text


    for i in range(5):
        ed_user = User('ed', 'Ed Jones', '3d5_p455w0r6')
        ed_user.comment = Comment('hey%s' % i)
        test.add(ed_user)

    d = D.comment.text == 'hey1'
    print d
    for u in test(D.comment.text == 'hey1'):
        print "'%s'" % u
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\underverse\tests\load_tests.py
# Compiled at: 2012-02-20 13:15:38
from underverse import Underverse
from underverse.model import Document
from test_data_gen import Person
import datetime, unittest, os

class AnotherTestClass(object):
    """docstring for AnotherTestClass"""

    def __init__(self, text):
        super(AnotherTestClass, self).__init__()
        self.a = Comment(text)
        self.msg = Message(2, 3, 4)
        self.array = range(3)


class Comment(object):
    """docstring for Comment"""

    def __init__(self, text):
        super(Comment, self).__init__()
        self.text = text

    def len(self):
        return len(self.text)


class Message(object):
    """docstring for Message"""

    def __init__(self, x, y, z, **kwargs):
        super(Message, self).__init__()
        self.x = x
        self.y = y
        self.z = z
        try:
            import numpy as np
            self.n = np.arange(5)
        except ImportError as e:
            self.n = range(5)

        self.m = Comment('Starting to come together')


class LoadTestCase(unittest.TestCase):

    def setUp(self):
        self.uv = Underverse()

    def tearDown(self):
        self.uv.close()

    def test_create_verse(self):
        self.users = self.uv.users
        self.assertIn(self.users._name, self.uv)

    def test_load_dict(self):
        self.users = self.uv.users
        user = {'name': 'ed', 'fullname': 'Ed Jones', 'password': '3d5_p455w0r6'}
        self.users.add(user)
        u = self.users.find_one(Document.name == 'ed', Document.password == '3d5_p455w0r6', Document.fullname == 'Ed Jones')
        self.assertTrue(u['name'] == user['name'] and u['fullname'] == user['fullname'] and u['password'] == user['password'])

    def test_load_dict_len(self):
        self.users = self.uv.users
        user = {'name': 'ed', 'fullname': 'Ed Jones', 'password': '3d5_p455w0r6'}
        self.users.add(user)
        self.assertTrue(len(self.users) == 1)

    def test_load_multiple_objs(self):
        self.users = self.uv.users
        for person in range(50):
            self.users.add(Person())

        self.assertTrue(len(self.users) == 50)

    def test_bulk_load(self):
        self.users = self.uv.users
        self.users.add([ Person() for i in range(50) ])
        self.assertTrue(len(self.users) == 50)

    def test_dump(self):
        self.users = self.uv.users
        self.users.add([ Person() for i in range(50) ])
        self.uv.dump('test.sql')
        self.assertTrue(os.path.exists('test.sql'))

    def test_load(self):
        self.uv.load('test.sql')
        self.assertTrue(len(self.uv.users) == 50)

    def test_load_large(self):
        self.uv.load('speed_test_smaller.sql')
        self.assertTrue(len(self.uv.test) == 250)

    def test_update(self):
        self.users = self.uv.users
        user = {'name': 'ed', 'fullname': 'Ed Jones', 'password': '3d5_p455w0r6'}
        self.users.add(user)
        u = self.users.find_one(Document.name == 'ed', Document.password == '3d5_p455w0r6', Document.fullname == 'Ed Jones')
        u.age = 25
        self.users.update(u)
        u = self.users.find_one(Document.name == 'ed', Document.password == '3d5_p455w0r6', Document.fullname == 'Ed Jones')
        self.assertTrue(hasattr(u, 'age') and u.age == 25)

    def test_update_list(self):
        self.users = self.uv.users
        user = {'name': 'ed', 'fullname': 'Ed Jones', 'password': '3d5_p455w0r6'}
        self.users.add(user)
        u = self.users.find_one(Document.name == 'ed', Document.password == '3d5_p455w0r6', Document.fullname == 'Ed Jones')
        u.friends = ['Michael', 'Luke', 'Amy']
        self.users.update(u)
        u = self.users.find_one(Document.name == 'ed', Document.password == '3d5_p455w0r6', Document.fullname == 'Ed Jones')
        self.assertTrue(hasattr(u, 'friends') and type(u.friends) == list and len(u.friends) == 3)

    def test_update_np_array(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest('NumPy not installed')

        self.users = self.uv.users
        user = {'name': 'ed', 'fullname': 'Ed Jones', 'password': '3d5_p455w0r6'}
        self.users.add(user)
        u = self.users.find_one(Document.name == 'ed', Document.password == '3d5_p455w0r6', Document.fullname == 'Ed Jones')
        u.list = np.arange(5)
        self.users.update(u)
        u = self.users.find_one(Document.name == 'ed', Document.password == '3d5_p455w0r6', Document.fullname == 'Ed Jones')
        self.assertTrue(hasattr(u, 'list') and type(u.list) == np.ndarray)

    def test_add_json_ext(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest('NumPy not installed')

        test = True
        try:
            Underverse.add_json_ext(np.ndarray, lambda obj: obj.tolist(), lambda obj: np.array(obj))
        except:
            raise
            true = False

        self.assertTrue(test)

    def test_load_and_read_objects(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest('NumPy not installed')

        test = self.uv.test
        test.add(AnotherTestClass('test #1'))
        good = True
        from underverse import NecRow
        for r in test:
            if not (type(r) == AnotherTestClass or type(r) == NecRow):
                good = False
            if not type(r.a) == Comment:
                good = False
            if not type(r.msg.n) == np.ndarray:
                good = False
            if not type(r.msg.m) == Comment:
                good = False
            if not type(r.msg) == Message:
                good = False

        self.assertTrue(good)

    def test_dump_objects(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest('NumPy not installed')

        test = self.uv.test
        test.add(AnotherTestClass('test #1'))
        self.uv.dump('obj_testing.sql')
        self.assertTrue(True)

    def test_load_objects(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest('NumPy not installed')

        self.uv.load('obj_testing.sql')
        good = True
        from underverse import NecRow
        for r in self.uv.test:
            if not (type(r) == AnotherTestClass or type(r) == NecRow):
                good = False
            if not type(r.a) == Comment:
                good = False
            if not type(r.msg.n) == np.ndarray:
                good = False
            if not type(r.msg.m) == Comment:
                good = False
            if not callable(r.msg.m.len):
                good = False
            if not type(r.msg) == Message:
                good = False

        self.assertTrue(good)

    def test_load_example(self):
        table = self.uv.helion
        table.add({'a': 1, 'b': 2})
        array = [{'a': 1, 'b': 2, 'c': 3}, {'a': 4, 'b': 5, 'c': 6}, {'a': 7, 'b': 8, 'c': 9}]
        table.add(array)
        self.assertTrue(True)

    def test_load_add_column(self):
        table = self.uv.data
        array = [{'a': 1, 'b': 2, 'c': 3}, {'a': 4, 'b': 5, 'c': 6}, {'a': 7, 'b': 8, 'c': 9}]
        table.add(array)
        table.add_column([1, 2, 3], 'd')
        self.assertTrue(len(list(table.d)) == 3)

    def test_load_array(self):
        table = self.uv.data
        array = [
         [
          1, 2, 3], [4, 5, 6], [7, 8, 9]]
        table.from_array(array, names=['x', 'y', 'z'])
        self.assertTrue(len(list(table.x)) == 3)

    def test_load_datetime(self):
        table = self.uv.data
        dt = datetime.datetime.now()
        table.add({'datetime': dt})
        self.assertTrue(len(list(table.datetime)) == 1)
        d = table.find_one()
        self.assertTrue(type(d.datetime) == datetime.datetime)

    def test_load_date(self):
        table = self.uv.data2
        dt = datetime.datetime.now().date()
        table.add({'date': dt})
        self.assertTrue(len(list(table.date)) == 1)
        d = table.find_one()
        self.assertTrue(type(d.date) == datetime.date)

    def test_load_time(self):
        table = self.uv.data2
        dt = datetime.datetime.now().time()
        table.add({'time': dt})
        self.assertTrue(len(list(table.time)) == 1)
        d = table.find_one()
        self.assertTrue(type(d.time) == datetime.time)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LoadTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
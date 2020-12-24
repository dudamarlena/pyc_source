# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\underverse\tests\find_tests.py
# Compiled at: 2012-02-21 17:19:18
from underverse import Underverse
from underverse.model import Document
from underverse.predicates import Predicate as P
from test_data_gen import Person
import unittest, os

class Comment(object):
    """docstring for Comment"""

    def __init__(self, text):
        super(Comment, self).__init__()
        self.text = text


class User(object):

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password


class FindTestCase(unittest.TestCase):

    def setUp(self):
        self.uv = Underverse()
        self.uv.load('speed_test_smaller.sql')

    def tearDown(self):
        self.uv.close()

    def test_find_one(self):
        self.test = self.uv.test
        me = self.uv.test.find_one(Document.name == 'Max')
        self.assertTrue(me.name == 'Max')

    def test_eq(self):
        eq = True
        ppl = self.uv.test.find(Document.name == 'Max')
        for person in ppl:
            if person.name != 'Max':
                eq = False

        self.assertTrue(eq)

    def test_ne(self):
        test = True
        ppl = self.uv.test.find(Document.name != 'Max')
        for person in ppl:
            if person.name == 'Max':
                test = False

        self.assertTrue(test)

    def test_lt(self):
        test = True
        ppl = self.uv.test.find(Document.name < 27)
        for person in ppl:
            if person.name >= 27:
                test = False

        self.assertTrue(test)

    def test_lte(self):
        test = True
        ppl = self.uv.test.find(Document.name <= 27)
        for person in ppl:
            if person.name > 27:
                test = False

        self.assertTrue(test)

    def test_gt(self):
        test = True
        ppl = self.uv.test.find(Document.name > 27)
        for person in ppl:
            if person.name <= 27:
                test = False

        self.assertTrue(test)

    def test_gte(self):
        test = True
        ppl = self.uv.test.find(Document.name >= 27)
        for person in ppl:
            if person.name < 27:
                test = False

        self.assertTrue(test)

    def test_len(self):
        test = True
        ppl = self.uv.test.find(Document.name.len(3))
        for person in ppl:
            if len(person.name) != 3:
                test = False

        self.assertTrue(test)

    def test_btw(self):
        test = True
        ppl = self.uv.test.find(Document.age.btw(18, 25))
        for person in ppl:
            if person.age <= 18 and person.age <= 25:
                test = False

        self.assertTrue(test)

    def test_in(self):
        test = True
        ppl = self.uv.test.find(Document.age.in_([18, 25]))
        for person in ppl:
            if person.age not in (18, 25):
                test = False

        self.assertTrue(test)

    def test_nin(self):
        test = True
        ppl = self.uv.test.find(Document.age.nin([18, 25]))
        for person in ppl:
            if person.age in (18, 25):
                test = False

        self.assertTrue(test)

    def test_match(self):
        import random, re
        test = True
        ips = self.uv.ips
        for i in range(250):
            ips.add({'ip': ('.').join(str(random.randint(0, 255)) for i in range(4))})

        ppl = ips.find(Document.ip.match('^\\d+\\.\\d+\\.\\d+\\.\\d+$'))
        for ip in ips:
            if not re.compile('^\\d+\\.\\d+\\.\\d+\\.\\d+$').match(ip.ip):
                test = False

        self.assertTrue(test)

    def test_match2(self):
        import random, re
        test = True
        ips = self.uv.ips
        for i in range(250):
            ips.add({'ip': ('.').join(str(random.randint(0, 255)) for i in range(4)) + '@8080'})

        ppl = ips.find(Document.ip.match('^\\d+\\.\\d+\\.\\d+\\.\\d+$'))
        for ip in ips:
            if not re.compile('^\\d+\\.\\d+\\.\\d+\\.\\d+$').match(ip.ip):
                test = False

        self.assertFalse(test)

    def test_search(self):
        import random, re
        test = True
        ips = self.uv.ips
        for i in range(250):
            ips.add({'ip': ('.').join(str(random.randint(0, 255)) for i in range(4)) + '@8080'})

        ppl = ips.find(Document.ip.search('\\d+\\.\\d+\\.\\d+\\.\\d+'))
        for ip in ips:
            if not re.compile('\\d+\\.\\d+\\.\\d+\\.\\d+').search(ip.ip):
                test = False

        self.assertTrue(test)

    def test_orderby(self):
        test = True
        ppl = self.uv.test.find(Document.orderby('age'))
        age = -1
        for person in ppl:
            if person.age < age:
                test = False
            age = person.age

        self.assertTrue(test)

    def test_orderby2(self):
        test = True
        ppl = self.uv.test.find(Document.orderby('-age'))
        age = 100
        for person in ppl:
            if person.age > age:
                test = False
            age = person.age

        self.assertTrue(test)

    def test_orderby3(self):
        test = True
        ppl = self.uv.test.find(Document.orderby('name', '-age', 'college'))
        age = 100
        name = 'aa'
        for person in ppl:
            if person.name < name:
                test = False
            if person.name != name:
                age = 100
            if person.age > age:
                test = False
            age = person.age

    def test_orderby4(self):
        test = True
        ppl = self.uv.test.find(Document.orderby())
        prev = ''
        for person in ppl:
            if str(person) < prev:
                test = False
            prev = str(person)

    def test_orderby5(self):
        test = True
        ppl = self.uv.test.orderby('name')
        prev = ''
        for person in ppl:
            if person.name < prev:
                test = False
            prev = person.name

        self.assertTrue(test)

    def test_orderby6(self):
        test = True
        ppl = self.uv.test.orderby('name', '-age', 'college')
        age = 100
        name = 'aa'
        for person in ppl:
            if person.name < name:
                test = False
            if person.name != name:
                age = 100
            if person.age > age:
                test = False
            age = person.age

    def test_orderby7(self):
        test = True
        ppl = self.uv.test.all().orderby('name', '-age', 'college')
        age = 100
        name = 'aa'
        for person in ppl:
            if person.name < name:
                test = False
            if person.name != name:
                age = 100
            if person.age > age:
                test = False
            age = person.age

    def test_orderby8(self):
        test = True
        ppl = self.uv.test.find(Document.age > 25).orderby('name', '-age', 'college')
        age = 100
        name = 'aa'
        for person in ppl:
            if person.name < name:
                test = False
            if person.name != name:
                age = 100
            if person.age > age:
                test = False
            age = person.age

    def test_find_all(self):
        self.test = self.uv.test
        length = len(list(self.test))
        results = self.test.find()
        self.assertTrue(len(list(results)) == length)

    def test_find_call(self):
        self.test = self.uv.test
        length = len(list(self.test.find(Document.name == 'Max')))
        results = self.test(Document.name == 'Max')
        self.assertTrue(len(list(results)) == length)

    def test_find_limit(self):
        self.test = self.uv.test
        results = self.test.find(Document.limit(5))
        self.assertTrue(len(list(results)) == 5)

    def test_find_skip(self):
        self.test = self.uv.test
        length = len(list(self.test))
        results = self.test.find(Document.skip(5))
        self.assertTrue(len(list(results)) == length - 5)

    def test_limit(self):
        self.test = self.uv.test
        results = self.test.limit(5)
        self.assertTrue(len(list(results)) == 5)

    def test_skip(self):
        self.test = self.uv.test
        length = len(list(self.test))
        results = self.test.skip(5)
        self.assertTrue(len(list(results)) == length - 5)

    def test_limit_skip(self):
        self.test = self.uv.test
        results = self.test.limit(5).skip(2)
        self.assertTrue(len(list(results)) == 3)

    def test_skip_limit(self):
        self.test = self.uv.test
        results = self.test.skip(5).limit(2)
        self.assertTrue(len(list(results)) == 2)

    def test_get_attr(self):
        self.test = self.uv.test
        names = list(self.test.all().name)
        self.assertTrue(type(names) == list and len(names) == 250)

    def test_get_nested(self):
        self.test = self.uv.test2
        for i in range(5):
            ed_user = User('ed', 'Ed Jones', '3d5_p455w0r6')
            ed_user.comment = Comment('hey%s' % i)
            self.test.add(ed_user)

        u = self.test.find(Document.comment.text == 'hey1')
        self.assertTrue(u != None)
        for i in u:
            self.assertTrue(i.comment.text == 'hey1')

        return

    def test_get_nested2(self):
        self.test2 = self.uv.test2
        for i in range(5):
            ed_user = User('ed', 'Ed Jones', '3d5_p455w0r6')
            ed_user.comment = Comment('hey%s' % i)
            self.test2.add(ed_user)

        from underverse.model import Document as D
        u = self.test2.find_one(Document.comment.text == 'hey1')
        self.assertTrue(u != None)
        self.assertTrue(u.comment.text == 'hey1')
        return

    def test_and(self):
        test = self.uv.test
        from underverse.predicates import AND
        r = test.find(AND(Document.name == 'Max', Document.age < 25))
        for x in r:
            self.assertTrue(x.name == 'Max' and x.age < 25)

    def test_or(self):
        test = self.uv.test
        from underverse.predicates import OR
        r = test.find(OR(Document.name == 'Max', Document.name == 'Zaphod'))
        for x in r:
            self.assertIn(x.name, ['Max', 'Zaphod'])

    def test_complex_andor(self):
        test = self.uv.test
        from underverse.predicates import AND, OR
        r = test.find(OR(Document.age.btw(30, 35), Document.age.btw(60, 65)))
        for x in r:
            self.assertTrue(x.age > 30 and x.age < 35 or x.age > 60 and x.age < 65)

    def test_complex_andor2(self):
        test = self.uv.test
        from underverse.predicates import AND, OR
        r = test.find(OR(Document.age.btw(30, 35), Document.age.btw(60, 65)), OR(Document.name == 'Billy', Document.name == 'Zaphod'))
        for x in r:
            self.assertTrue(x.age > 30 and x.age < 35 or x.age > 60 and x.age < 65)
            self.assertIn(x.name, ['Billy', 'Zaphod'])

    def test_complex_andor3(self):
        test = self.uv.test
        from underverse.predicates import AND, OR
        r = test.find(OR(AND(Document.name == 'Zaphod', Document.age.btw(60, 65)), AND(Document.name == 'Billy', Document.age == 31)))
        for x in r:
            self.assertTrue(x.age > 30 and x.age < 35 or x.age > 60 and x.age < 65)
            self.assertIn(x.name, ['Billy', 'Zaphod'])

    def test_paginate(self):
        test = self.uv.test_paging
        for i in range(15):
            test.add({'a': i, 'b': i * 2, 'c': i * 3})

        for page in test.paginate(5):
            self.assertTrue(len(page) == 5)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FindTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    exit()
    import json, numpy as np, time, random
    from underverse import NecRow
    uv = Underverse()

    class AnotherTestClass(object):
        """docstring for AnotherTestClass"""

        def __init__(self, text):
            super(AnotherTestClass, self).__init__()
            self.a = Comment(text)
            self.msg = Message(2, 3, 4)
            self.array = range(3)

        def _sum(self, value):
            return sum(self.array) + value


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
            self.n = np.arange(5)
            self.m = Comment('Starting to come together')


    msg = Message(1, 2, 3)
    print msg.m.len()
    print msg.__dict__
    test = uv.testing

    def udp(doc):
        if '1' in doc.text:
            return True
        return False


    data = []
    data.append(AnotherTestClass('test #1'))
    data.append(AnotherTestClass('test #2'))
    data.append(AnotherTestClass('test #3'))
    test.add(data)
    for r in test:
        print r.a.text
        print r._sum(5), r.array

    uv.dump('testing.sql')
    print 'Done.'
    exit()
    print
    import json, numpy as np
    data = [ Person().__dict__ for i in range(50000) ]
    import time
    test = uv.testing
    test.add(data)
    print len(test)
    start = time.time()
    qd = test.purify('name', 'age', 'gender')
    gb = qd.groupby('name')
    for name, ppl in gb:
        for age, ages in ppl.groupby('age'):
            print name, age, len(ages)

    print 'UV - QD: ', time.time() - start
    print
    start = time.time()
    gb = test.groupby('name')
    for name, ppl in gb:
        for age, ages in ppl.groupby('age'):
            print name, age, len(ages)

    print 'UV: ', time.time() - start
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_context.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import print_function
import unittest
from moya.context import Context
from moya.context import dataindex

class TestDataIndex(unittest.TestCase):

    def test_parse(self):
        """Test dataindex parse"""
        tests = [
         (
          b'', []),
         (
          b'.', []),
         (
          b'""', [b'']),
         (
          b'\\\\', [b'\\']),
         (
          b'foo', [b'foo']),
         (
          b'foo.bar', [b'foo', b'bar']),
         (
          b'.foo.bar', [b'foo', b'bar']),
         (
          b'foo.bar.baz', [b'foo', b'bar', b'baz']),
         (
          b'"foo"', [b'foo']),
         (
          b'"foo".bar', [b'foo', b'bar']),
         (
          b'"foo.bar"', [b'foo.bar']),
         (
          b'foo\\.bar', [b'foo.bar']),
         (
          b'1', [1]),
         (
          b'"1"', [b'1']),
         (
          b'foo.2', [b'foo', 2])]
        for index, parsed in tests:
            self.assertEqual(dataindex.parse(index), parsed)

    def test_build(self):
        """Test encoding indices as a dataindex string"""
        self.assertEqual(dataindex.build([b'Hello', b'World', 1]), b'Hello.World.1')
        self.assertEqual(dataindex.build([b'Hello']), b'Hello')

    def test_join(self):
        """Test joining of indices"""
        self.assertEqual(dataindex.join(b'foo'), b'foo')
        self.assertEqual(dataindex.join(b'foo', b'bar.baz'), b'foo.bar.baz')
        self.assertEqual(dataindex.join(b'foo', b'bar\\.baz'), b'foo."bar.baz"')
        self.assertEqual(dataindex.join(b'foo', b'"bar.baz"'), b'foo."bar.baz"')
        self.assertEqual(dataindex.join(b'foo', b'bar.baz.1:5'), b'foo.bar.baz.1:5')
        self.assertEqual(dataindex.join(b'foo', b'bar', b'baz'), b'foo.bar.baz')
        self.assertEqual(dataindex.join(b'foo', [b'bar', b'baz']), b'foo.bar.baz')
        self.assertEqual(dataindex.join(b'.foo', b'bar', b'baz'), b'.foo.bar.baz')
        self.assertEqual(dataindex.join(b'foo', b'.bar', b'baz'), b'.bar.baz')

    def test_normalize(self):
        """Test normalizing indices"""
        self.assertEqual(dataindex.normalize(b'foo'), b'foo')
        self.assertEqual(dataindex.normalize(b'\\foo'), b'foo')
        self.assertEqual(dataindex.normalize(b'\\f\\o\\o'), b'foo')
        self.assertEqual(dataindex.normalize(b'"foo"'), b'foo')

    def test_make_absolute(self):
        """Test making a data index absolute"""
        self.assertEqual(dataindex.make_absolute(b'foo.bar'), b'.foo.bar')
        self.assertEqual(dataindex.make_absolute(b'.foo.bar'), b'.foo.bar')

    def test_iter_index(self):
        """Test iter_index method"""
        self.assertEqual(list(dataindex.iter_index(b'foo.bar.baz')), [('foo', 'foo'),
         ('bar', 'foo.bar'),
         ('baz', 'foo.bar.baz')])


class TestContext(unittest.TestCase):

    def setUp(self):
        pass

    def test_basic_root(self):
        """Test basic operations from root"""
        c = Context()
        c[b'foo'] = b'bar'
        self.assert_(b'foo' in c)
        self.assertEqual(c[b'foo'], b'bar')
        self.assertEqual(c.root[b'foo'], b'bar')
        c[b'fruit'] = b'apple'
        self.assert_(b'fruit' in c)
        self.assertEqual(c[b'fruit'], b'apple')
        self.assertEqual(c.root[b'fruit'], b'apple')
        self.assertEqual(c.get(b'nothere', b'missing'), b'missing')
        self.assertEqual(sorted(c.keys()), [b'foo', b'fruit'])
        self.assertEqual(sorted(c.values()), [b'apple', b'bar'])
        self.assertEqual(sorted(c.items()), [('foo', 'bar'), ('fruit', 'apple')])

    def test_attr(self):
        """Test attribute / getitem distinction"""

        class A(object):
            foo = b'buzz'
            bar = b'cantsee'

            def __getitem__(self, key):
                if key == b'foo':
                    return b'baz'
                raise IndexError(key)

            def __contains__(self, key):
                return key == b'foo'

        c = Context()
        c[b'a'] = A()
        self.assertEqual(c[b'a.foo'], b'baz')
        self.assert_(c[b'a.bar'].moya_missing)
        self.assert_(b'a.bar' not in c)
        self.assert_(b'a.foo' in c)

    def test_get_root(self):
        """Test looking up root object"""
        c = Context({b'foo': [1, 2, 3]})
        self.assertEqual(c[b''], {b'foo': [1, 2, 3]})
        c.push_frame(b'foo')
        self.assertEqual(c[b''], [1, 2, 3])
        c.push_frame(b'.foo')
        self.assertEqual(c[b''], [1, 2, 3])
        c.push_frame(b'.')
        self.assertEqual(c[b''], {b'foo': [1, 2, 3]})

    def test_inspect(self):
        """Test keys/values/items"""
        c = Context()
        c[b'foo'] = dict(a=1, b=2, c=3)
        c[b'bar'] = [b'a', b'b', b'c']

        def compare(a, b):
            a = sorted(a, key=lambda k: str(k.__class__.__name__))
            b = sorted(b, key=lambda k: str(k.__class__.__name__))
            for compare_a, compare_b in zip(a, b):
                self.assertEqual(compare_a, compare_b)

        self.assertEqual(sorted(c.keys()), [b'bar', b'foo'])
        self.assertEqual(sorted(c.keys(b'foo')), [b'a', b'b', b'c'])
        self.assertEqual(sorted(c.keys(b'bar')), [0, 1, 2])
        compare(c.values(), [dict(a=1, b=2, c=3), [b'a', b'b', b'c']])
        self.assertEqual(sorted(c.values(b'foo')), [1, 2, 3])
        self.assertEqual(sorted(c.values(b'bar')), [b'a', b'b', b'c'])
        compare(sorted(c.items()), sorted([(b'foo', dict(a=1, b=2, c=3)), (b'bar', [b'a', b'b', b'c'])]))
        self.assertEqual(sorted(c.items(b'foo')), [('a', 1), ('b', 2), ('c', 3)])
        self.assertEqual(sorted(c.items(b'bar')), [(0, 'a'), (1, 'b'), (2, 'c')])
        self.assertEqual(sorted(c.all_keys()), sorted([b'', b'foo', b'foo.a', b'foo.c', b'foo.b', b'bar', b'bar.0', b'bar.1', b'bar.2']))

    def test_frame_stack(self):
        """Test push/pop frame operations"""
        c = Context()
        c[b'foo'] = {}
        c.push_frame(b'foo')
        self.assertEqual(c.get_frame(), b'.foo')
        c[b'bar'] = 1
        self.assertEqual(c.root[b'foo'][b'bar'], 1)
        c.pop_frame()
        self.assertEqual(c.get_frame(), b'.')
        c[b'baz'] = 2
        self.assertEqual(c.root[b'baz'], 2)

    def test_root_indices(self):
        """Test root indices"""
        c = Context()
        c[b'foo'] = {}
        c[b'baz'] = 2
        c.push_frame(b'foo')
        c[b'bar'] = 1
        self.assertEqual(c[b'.baz'], 2)
        self.assertEqual(c[b'bar'], 1)
        c.push_frame(b'.')
        self.assertEqual(c[b'baz'], 2)
        self.assertEqual(c[b'foo.bar'], 1)
        c.pop_frame()
        self.assertEqual(c[b'.baz'], 2)
        self.assertEqual(c[b'bar'], 1)
        self.assertEqual(c[b'.foo.bar'], 1)

    def test_expressions(self):
        """Test expression evaluation"""
        c = Context()
        c[b'foo'] = {}
        c[b'baz'] = 2
        c[b'foo.a'] = 10
        c[b'foo.b'] = 20
        c[b'foo.c'] = dict(inception=b'three levels')
        c[b'word'] = b'apples'
        c[b'word2'] = c[b'word']
        c[b'lt'] = b'less than'

        class ChoiceTest(object):

            def __init__(self):
                self.choices = []

        c[b'choicetest'] = ChoiceTest()

        class Obj(object):

            def __init__(self, id):
                self.id = id

        c[b'objects'] = [
         Obj(1), Obj(2), Obj(3)]
        tests = [
         ('1', 1),
         ('123', 123),
         ('"1"', '1'),
         ("'1'", '1'),
         ('"\\""', '"'),
         ("'''1'''", '1'),
         ('"""1"""', '1'),
         ('100-5', 95),
         ('7//2', 3),
         ('1+1', 2),
         ('1+2+3', 6),
         ('2+3*2', 8),
         ('(2+3)*2', 10),
         ('foo.a', 10),
         ('$foo.a', 10),
         ('$lt', 'less than'),
         ('foo.c.inception', 'three levels'),
         ('foo.a+foo.b', 30),
         ('.foo.a+.foo.b', 30),
         ('foo.a/2', 5),
         ('foo.a/4', 2.5),
         ('word*3', 'applesapplesapples'),
         ('word.2*3', 'ppp'),
         ('word+str:2', 'apples2'),
         (
          b'word^="a"', True),
         (
          b'word^="app"', True),
         (
          b'word^="ppa"', False),
         (
          b'word$="les"', True),
         (
          b'word$="s"', True),
         (
          b'2!=3', True),
         (
          b'2>1', True),
         (
          b'1<2', True),
         (
          b'1>2', False),
         (
          b'3<1', False),
         (
          b'1==1', True),
         (
          b'10>=10', True),
         (
          b'9.9<=10', True),
         (
          b'foo.a==10', True),
         (
          b'foo.a=="a"', False),
         (
          b"foo.a=='a'", False),
         (
          b'3*2>5', True),
         (
          b'2 gt 1', True),
         (
          b'1 lt 2', True),
         (
          b'1 gt 2', False),
         (
          b'3 lt 1', False),
         (
          b'10 gte 10', True),
         (
          b'9.9 lte 10', True),
         (
          b'3*2 gt 5', True),
         ('None', None),
         (
          b'True', True),
         (
          b'False', False),
         (
          b'yes', True),
         (
          b'no', False),
         ('int:"3"', 3),
         ('str:50', '50'),
         ('float:"2.5"', 2.5),
         (
          b'bool:"test"', True),
         (
          b'bool:1', True),
         (
          b'bool:""', False),
         (
          b'isint:5', True),
         (
          b'isint:"5"', False),
         (
          b'isnumber:2', True),
         (
          b'isnumber:2.5', True),
         (
          b'isnumber:"a"', False),
         (
          b'isfloat:1.0', True),
         (
          b'isfloat:1', False),
         (
          b'isstr:1', False),
         (
          b'isstr:"a"', True),
         (
          b'isbool:True', True),
         (
          b'isbool:False', True),
         (
          b'isbool:(2+1)', False),
         (
          b'isbool:bool:1', True),
         (
          b'isbool:bool:0', True),
         ('len:word', 6),
         (
          b'True and True', True),
         (
          b'False and False', False),
         (
          b'True or False', True),
         (
          b'False or False', False),
         (
          b'word=="apples"', True),
         (
          b'1==2 or word=="apples"', True),
         (
          b"'a' in 'apples'", True),
         (
          b"'ppl' in 'apples'", True),
         (
          b'word.1==word.2', True),
         (
          b'word is word2', True),
         (
          b"'index.html' fnmatches '*.html'", True),
         (
          b"'foo/index.html' fnmatches '*.html'", True),
         (
          b"'index.html' fnmatches '*.py'", False),
         (
          b"'index.html' fnmatches '*.h??l'", True),
         (
          b"'hello, world' matches /.*world/", True),
         (
          b"'hello, will' matches /.*world/", False),
         (
          b"'hello, world' matches '.*world'", True),
         (
          b"'hello, will' matches '.*world'", False),
         (
          b"'inception' in foo['c']", True),
         (
          b"'inception' in (foo['c'])", True),
         (
          b'exists:foo', True),
         (
          b'exists:baz', True),
         (
          b'exists:asdfsadf', False),
         (
          b'missing:foo', False),
         (
          b'missing:nobodyherebutuschickens', True),
         (
          b'missing:yesterday', True),
         (
          b'missing:foo.bar.baz', True),
         (
          b'missing:andrew', True),
         (
          b"'1' instr [1,2,3,4]", True),
         (
          b"'5' instr [1,2,3,4]", False),
         (
          b"'1' not instr [1,2,3,4]", False),
         (
          b"'5' not instr [1,2,3,4]", True),
         (
          b'1 in None', False),
         (
          b'1 instr None', False),
         (
          b'a=1', {b'a': 1}),
         (
          b'{"a":1}', {b'a': 1}),
         (
          b'[1,2,3]', [1, 2, 3]),
         (
          b'[1,2,3,[4,5,6]]', [1, 2, 3, [4, 5, 6]]),
         (
          b'[1,2,3,[4,5,6,[7,8,9]]]', [1, 2, 3, [4, 5, 6, [7, 8, 9]]]),
         (
          b'[1]', [1]),
         (
          b'[]', []),
         ("d:'5'", 5),
         ("d:'5' + 1", 6),
         ("d:'5' + d:'1'", 6),
         ('debug:d:5', "d:'5'"),
         ('filesize:1024', '1.0 KB'),
         ('abs:-3.14', 3.14),
         ('basename:"/foo/bar/baz"', 'baz'),
         (
          b'bool:""', False),
         ('capitalize:"hello"', 'Hello'),
         ('ceil:3.14', 4),
         (
          b'choices:choicetest', []),
         (
          b'chain:[[1, 2], [3, 4]]', [1, 2, 3, 4]),
         ('chr:65', 'A'),
         (
          b"collect:[['hello', 'world'], 0]", [b'h', b'w']),
         (
          b"sorted:items:collectmap:[['hello', 'world'], 0]", [('h', 'hello'), ('w', 'world')]),
         (
          b'collectids:objects', [1, 2, 3]),
         ("commalist:['hello', 'world']", 'hello,world'),
         ("commaspacelist:['hello', 'world']", 'hello, world'),
         ("'hello\\nworld'", 'hello\nworld'),
         ('\'you can \\"quote me\\" on that\'', 'you can "quote me" on that'),
         ("'\\\\'", '\\'),
         ("'helloworld'[1]", 'e'),
         ("'helloworld'[-1]", 'd'),
         ("'helloworld'[:2]", 'he'),
         ("'helloworld'[2:4]", 'll'),
         ("'helloworld'[::-1]", 'dlrowolleh')]
        for expression, result in tests:
            print(expression, result)
            expression_result = c.eval(expression)
            print(b'\t', expression_result)
            self.assertEqual(expression_result, result)

        return

    def test_expression_index(self):
        """Test the index operator"""
        c = Context()
        c[b'foo'] = {}
        c[b'baz'] = 2
        c[b'foo.a'] = 10
        c[b'foo.b'] = 20
        c[b'foo.c'] = dict(inception=b'three levels')
        c[b'word'] = b'apples'
        c[b'word2'] = c[b'word']
        c[b'lt'] = b'less than'

        class Obj(object):

            def __init__(self):
                self.n = 123
                self.foo = [b'Hello', b'World', b'!']

        c[b'o'] = Obj()
        tests = [
         ('"apples"[0]', 'a'),
         ('"apples"[1]', 'p'),
         ('"apples"[1+2]', 'l'),
         ('"apples"[-1]', 's'),
         ('foo["a"]', 10),
         ('foo["b"]', 20),
         (
          b'foo["c"]', dict(inception=b'three levels')),
         ('foo["c"]["inception"]', 'three levels'),
         ('foo.c["inception"]', 'three levels'),
         ('foo.c["inception"][1]', 'h'),
         ('o["n"]', 123),
         ('o["foo"][1]', 'World')]
        for expression, result in tests:
            print(expression)
            expression_result = c.eval(expression)
            self.assertEqual(expression_result, result)

    def test_expression_filter(self):
        """Test filter evaluation"""
        c = Context()
        c[b'filter'] = dict(double=lambda v: v * 2, square=lambda v: v * v)
        c[b'data'] = dict(a=1, b=10, c=123)
        tests = [
         ('3|filter.double', 6),
         ('3|.filter.double', 6),
         ('data.a + data.b|filter.double', 22),
         ('(data.a + data.b)|filter.double', 22),
         ('3|filter.square', 9),
         ('3|filter.double|filter.square', 36)]
        for expression, result in tests:
            print(expression)
            expression_result = c.eval(expression)
            self.assertEqual(expression_result, result)

    def test_expressions_with_fame(self):
        """Test expression evaluation in a frame"""
        c = Context()
        c[b'foo'] = dict(a=1, b=2, bar=b'apples')
        c[b'top'] = 10
        c[b'r'] = list(range(10))
        tests = [('a+b', 3),
         ('.top', 10),
         ('a+.top', 11),
         ('.r.4+.top', 14)]
        with c.frame(b'foo'):
            for expression, result in tests:
                self.assertEqual(c.eval(expression), result)

    def test_set_lazy(self):
        """Test lazy evaluation"""
        c = Context()
        evaluations = [0]

        def add(a, b):
            evaluations[0] += 1
            return a + b

        c.set_lazy(b'foo', add, 3, 4)
        self.assertEqual(evaluations[0], 0)
        self.assertEqual(c[b'foo'], 7)
        self.assertEqual(evaluations[0], 1)
        self.assertEqual(c[b'foo'], 7)
        self.assertEqual(evaluations[0], 1)
        c.set_lazy(b'bar', lambda : {})
        self.assertEqual(c[b'bar'], {})

    def test_set_async(self):
        """Test asyncronous evaluation"""
        c = Context()
        c.set_async(b'foo', lambda : b'bar')
        self.assertEqual(c[b'foo'], b'bar')
        self.assertEqual(c[b'foo'], b'bar')

        def waiter(wait_time, result):
            import time
            time.sleep(wait_time)
            return result

        c.set_async(b'bestthings', waiter, 0.1, b'guiness')
        self.assertEqual(c[b'bestthings'], b'guiness')
        self.assertEqual(c[b'bestthings'], b'guiness')

    def test_set_new(self):
        """Test setting values if not present"""
        c = Context()
        c.set_new(b'foo', {})
        self.assertEqual(c[b'foo'], {})
        c.set_new(b'foo', 100)
        self.assertEqual(c[b'foo'], {})

    def test_deleting(self):
        """Test deleting from context"""
        c = Context()
        c[b'foo'] = {}
        c[b'foo.bar'] = 1
        c[b'foo.baz'] = 2
        self.assert_(b'foo' in c)
        self.assert_(b'foo.bar' in c)
        self.assert_(b'foo.baz' in c)
        del c[b'foo.bar']
        self.assert_(b'foo' in c)
        self.assert_(b'foo.bar' not in c)
        self.assert_(b'foo.baz' in c)
        del c[b'foo']
        self.assert_(b'foo' not in c)
        self.assert_(b'foo.bar' not in c)
        self.assert_(b'foo.baz' not in c)

    def test_copy_move(self):
        """Test copying and moving values"""
        c = Context()
        c[b'foo'] = 123
        c[b'bar'] = {}
        c[b'bar.baz'] = 456
        c.copy(b'foo', b'foo2')
        self.assertEqual(c[b'foo'], 123)
        self.assertEqual(c[b'foo2'], 123)
        with c.frame(b'bar'):
            c.copy(b'baz', b'.zab')
        self.assertEqual(c[b'zab'], 456)
        c = Context()
        c[b'foo'] = 123
        c[b'bar'] = {}
        self.assert_(b'foo' in c)
        c.move(b'foo', b'bar.foo')
        self.assert_(b'foo' not in c)
        self.assert_(b'bar.foo' in c)
        self.assertEqual(c[b'bar.foo'], 123)

    def test_scope(self):
        """Test scope facility"""
        c = Context()
        c[b'foo'] = dict(a=1, b=2)
        c[b'bar'] = {}
        c.push_frame(b'.foo')
        self.assertEqual(c[b'a'], 1)
        self.assertEqual(c[b'b'], 2)
        self.assert_(b'c' not in c)
        c.push_scope(b'.bar')
        c[b'.bar.c'] = 3
        self.assert_(b'c' in c)
        self.assertEqual(c[b'c'], 3)
        c.pop_scope()
        self.assert_(b'c' not in c)
        self.assertEqual(c[b'a'], 1)
        self.assertEqual(c[b'b'], 2)

    def test_stack(self):
        c = Context()
        c.push_stack(b'content', b'foo')
        self.assertEqual(c[b'.content'], b'foo')
        c.push_stack(b'content', b'bar')
        self.assertEqual(c[b'.content'], b'bar')
        value = c.pop_stack(b'content')
        self.assertEqual(value, b'bar')
        self.assertEqual(c[b'.content'], b'foo')
        value = c.pop_stack(b'content')
        self.assertEqual(value, b'foo')
        self.assert_(c[b'.content'] is None)
        return
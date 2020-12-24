# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/regression.py
# Compiled at: 2017-12-12 16:52:26
import unittest, json
from transit.reader import Reader
from transit.writer import Writer
from transit.class_hash import ClassDict
from transit.transit_types import Symbol, frozendict, true, false, Keyword, Named
from transit.pyversion import unicode_type
from decimal import Decimal
from io import BytesIO, StringIO

class RegressionBaseTest(unittest.TestCase):
    pass


def regression(name, value):

    class RegressionTest(RegressionBaseTest):

        def test_roundtrip(self):
            in_data = value
            io = StringIO()
            w = Writer(io, 'json')
            w.write(in_data)
            r = Reader('json')
            out_data = r.read(StringIO(io.getvalue()))
            self.assertEqual(in_data, out_data)

    globals()['test_' + name + '_json'] = RegressionTest


regression('cache_consistency', ({'Problem?': true},
 Symbol('Here'),
 Symbol('Here')))
regression('one_pair_frozendict', frozendict({'a': 1}))
regression('json_int_max', (9007199254741092, 9223372036854775908))
regression('newline_in_string', 'a\nb')
regression('big_decimal', Decimal('190234710272.2394720347203642836434'))
regression('dict_in_set', frozenset(frozendict({'test': 'case'})))

def json_verbose_cache_bug():

    class JsonVerboseCacheBug(RegressionBaseTest):
        """Can't rely on roundtrip behavior to test this bug, have to
           actually verify that both keys are written for json_verbose
           behavior to be correct."""

        def test_key_not_cached(self):
            io = StringIO()
            w = Writer(io, 'json_verbose')
            w.write([{'myKey1': 42}, {'myKey1': 42}])
            self.assertEqual(io.getvalue(), '[{"myKey1":42},{"myKey1":42}]')

    globals()['test_json_verbose_cache_bug'] = JsonVerboseCacheBug


json_verbose_cache_bug()

def json_int_boundary(value, expected_type):

    class JsonIntBoundaryTest(unittest.TestCase):

        def test_max_is_number(self):
            for protocol in ('json', 'json_verbose'):
                io = StringIO()
                w = Writer(io, protocol)
                w.write([value])
                actual_type = type(json.loads(io.getvalue())[0])
                self.assertEqual(expected_type, actual_type)

    globals()['test_json_int_boundary_' + str(value)] = JsonIntBoundaryTest


json_int_boundary(9007199254740991, int)
json_int_boundary(9007199254740992, unicode_type)
json_int_boundary(-9007199254740991, int)
json_int_boundary(-9007199254740992, unicode_type)

class BooleanTest(unittest.TestCase):
    """Even though we're roundtripping transit_types.true and
    transit_types.false now, make sure we can still write Python bools.

    Additionally, make sure we can still do basic logical evaluation on transit
    Boolean values.
    """

    def test_write_bool(self):
        for protocol in ('json', 'json_verbose', 'msgpack'):
            io = BytesIO() if protocol is 'msgpack' else String()
            w = Writer(io, protocol)
            w.write((True, False))
            r = Reader(protocol)
            io.seek(0)
            out_data = r.read(io)
            assert out_data[0] == true
            assert out_data[1] == false

    def test_basic_eval(self):
        assert true
        assert not false

    def test_or(self):
        assert true or false
        assert not (false or false)
        assert true or true

    def test_and(self):
        assert not (true and false)
        assert true and true
        assert not (false and false)


class parent(object):
    pass


class child(parent):
    pass


class grandchild(child):
    pass


class ClassDictInheritanceTest(unittest.TestCase):
    """ Fix from issue #18: class_hash should iterate over all ancestors
    in proper mro, not just over direct ancestor.
    """

    def test_inheritance(self):
        cd = ClassDict()
        cd[parent] = 'test'
        assert grandchild in cd


class NamedTests(unittest.TestCase):
    """ Verify behavior for newly introduced built-in Named name/namespace
    parsing. Accomplished through transit_types.Named, a mixin for
    transit_types.Keyword and transit_types.Symbol.
    """

    def test_named(self):
        k = Keyword('blah')
        s = Symbol('blah')
        assert k.name == 'blah'
        assert s.name == 'blah'

    def test_namespaced(self):
        k = Keyword('ns/name')
        s = Symbol('ns/name')
        assert k.name == 'name'
        assert s.name == 'name'
        assert k.namespace == 'ns'
        assert s.namespace == 'ns'

    def test_slash(self):
        k = Keyword('/')
        s = Symbol('/')
        assert k.name == '/'
        assert s.name == '/'
        assert k.namespace is None
        assert s.namespace is None
        return


if __name__ == '__main__':
    unittest.main()
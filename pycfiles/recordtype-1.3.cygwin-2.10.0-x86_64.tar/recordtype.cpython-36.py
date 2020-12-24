# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/home/eric/local/recordtype/py3/lib/python3.6/site-packages/recordtype.py
# Compiled at: 2018-08-03 21:06:27
# Size of source mod 2**32: 22533 bytes
__all__ = [
 'recordtype', 'NO_DEFAULT']
import sys as _sys
from keyword import iskeyword as _iskeyword
from collections import Mapping as _Mapping
from six import exec_, string_types
NO_DEFAULT = object()

class _Fields(object):

    def __init__(self, default):
        self.default = default
        self.with_defaults = []
        self.without_defaults = []

    def add_with_default(self, field_name, default):
        if default is NO_DEFAULT:
            self.add_without_default(field_name)
        else:
            self.with_defaults.append((field_name, default))

    def add_without_default(self, field_name):
        if self.default is NO_DEFAULT:
            if self.with_defaults:
                raise ValueError('field {0} without a default follows fields with defaults'.format(field_name))
            self.without_defaults.append(field_name)
        else:
            self.add_with_default(field_name, self.default)


def _check_name(name, is_type_name=False, seen_names=None):
    if len(name) == 0:
        raise ValueError('Type names and field names cannot be zero length: {0!r}'.format(name))
    elif not all(c.isalnum() or c == '_' for c in name):
        raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: {0!r}'.format(name))
    else:
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a keyword: {0!r}'.format(name))
        if name[0].isdigit():
            raise ValueError('Type names and field names cannot start with a number: {0!r}'.format(name))
        if not is_type_name:
            if name in seen_names:
                raise ValueError('Encountered duplicate field name: {0!r}'.format(name))
            if name.startswith('_'):
                raise ValueError('Field names cannot start with an underscore: {0!r}'.format(name))


def _check_field_name(name, seen_names, rename, idx):
    try:
        _check_name(name, seen_names=seen_names)
    except ValueError as ex:
        if rename:
            return '_' + str(idx)
        raise

    seen_names.add(name)
    return name


def _default_name(field_name):
    return '_x_{0}_default'.format(field_name)


def recordtype(typename, field_names, default=NO_DEFAULT, rename=False, use_slots=True):
    fields = _Fields(default)
    _check_name(typename, is_type_name=True)
    if isinstance(field_names, string_types):
        field_names = field_names.replace(',', ' ').split()
    if isinstance(field_names, _Mapping):
        field_names = field_names.items()
    else:
        seen_names = set()
        for idx, field_name in enumerate(field_names):
            if isinstance(field_name, string_types):
                field_name = _check_field_name(field_name, seen_names, rename, idx)
                fields.add_without_default(field_name)
            else:
                try:
                    if len(field_name) != 2:
                        raise ValueError('field_name must be a 2-tuple: {0!r}'.format(field_name))
                except TypeError:
                    raise ValueError('field_name must be a 2-tuple: {0!r}'.format(field_name))

                default = field_name[1]
                field_name = _check_field_name(field_name[0], seen_names, rename, idx)
                fields.add_with_default(field_name, default)

        all_field_names = fields.without_defaults + [name for name, default in fields.with_defaults]
        argtxt = ', '.join(all_field_names)
        quoted_argtxt = ', '.join(repr(name) for name in all_field_names)
        if len(all_field_names) == 1:
            quoted_argtxt += ','
        initargs = ', '.join(fields.without_defaults + ['{0}={1}'.format(name, _default_name(name)) for name, default in fields.with_defaults])
        reprtxt = ', '.join('{0}={{{0}!r}}'.format(f) for f in all_field_names)
        dicttxt = ', '.join('{0!r}:self.{0}'.format(f) for f in all_field_names)
        if all_field_names:
            inittxt = '; '.join('self.{0}={0}'.format(f) for f in all_field_names)
            eqtxt = 'and ' + ' and '.join('self.{0}==other.{0}'.format(f) for f in all_field_names)
            itertxt = '; '.join('yield self.{0}'.format(f) for f in all_field_names)
            tupletxt = '(' + ', '.join('self.{0}'.format(f) for f in all_field_names) + ')'
            getstate = 'return ' + tupletxt
            setstate = tupletxt + ' = state'
        else:
            inittxt = 'pass'
            eqtxt = ''
            itertxt = 'return iter([])'
            getstate = 'return ()'
            setstate = 'pass'
        if use_slots:
            slotstxt = '__slots__ = _fields'
        else:
            slotstxt = ''
    template = 'class {typename}(object):\n        "{typename}({argtxt})"\n\n        _fields = ({quoted_argtxt})\n        {slotstxt}\n\n        def __init__(self, {initargs}):\n            {inittxt}\n\n        def __len__(self):\n            return {num_fields}\n\n        def __iter__(self):\n            {itertxt}\n\n        def _asdict(self):\n            return {{{dicttxt}}}\n\n        def __repr__(self):\n            return "{typename}(" + "{reprtxt}".format(**self._asdict()) + ")"\n\n        def __eq__(self, other):\n            return isinstance(other, self.__class__) {eqtxt}\n\n        def __ne__(self, other):\n            return not self==other\n\n        def __getstate__(self):\n            {getstate}\n\n        def __setstate__(self, state):\n            {setstate}\n'.format(typename=typename,
      argtxt=argtxt,
      quoted_argtxt=quoted_argtxt,
      initargs=initargs,
      inittxt=inittxt,
      dicttxt=dicttxt,
      reprtxt=reprtxt,
      eqtxt=eqtxt,
      num_fields=(len(all_field_names)),
      itertxt=itertxt,
      getstate=getstate,
      setstate=setstate,
      slotstxt=slotstxt)
    namespace = {}
    for name, default in fields.with_defaults:
        namespace[_default_name(name)] = default

    try:
        exec_(template, namespace, namespace)
    except SyntaxError as e:
        raise SyntaxError(e.message + ':\n' + template)

    cls = namespace[typename]
    cls._source = template
    if hasattr(_sys, '_getframe'):
        if _sys.platform != 'cli':
            cls.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
    return cls


if __name__ == '__main__':
    import unittest, pickle
    pickle_mods = [
     pickle]
    try:
        import cPickle
        pickle_mods.append(cPickle)
    except ImportError:
        pass

    TestRT0 = recordtype('TestRT0', '')
    TestRT = recordtype('TestRT', 'x y z')

    class TestRecordtype(unittest.TestCase):

        def test_simple(self):
            Point = recordtype('Point', 'x y')
            p = Point(10, 20)
            self.assertEqual((p.x, p.y), (10, 20))
            self.assertEqual(p._asdict(), {'x':10,  'y':20})
            Point = recordtype('Point', 'x,y')
            p = Point(10, 20)
            self.assertEqual((p.x, p.y), (10, 20))
            self.assertEqual(p._asdict(), {'x':10,  'y':20})
            Point = recordtype('Point', 'x, y')
            p = Point(10, 20)
            self.assertEqual((p.x, p.y), (10, 20))
            self.assertEqual(p._asdict(), {'x':10,  'y':20})
            Point = recordtype('Point', ['x', 'y'])
            p = Point(10, 20)
            self.assertEqual((p.x, p.y), (10, 20))
            self.assertEqual(p._asdict(), {'x':10,  'y':20})
            self.assertEqual(Point(10, 11), Point(10, 11))
            self.assertNotEqual(Point(10, 11), Point(10, 12))

        def test_bad_name(self):
            self.assertRaises(ValueError, recordtype, 'Point*', 'x y')
            self.assertRaises(ValueError, recordtype, 'Point', '# y')
            self.assertRaises(ValueError, recordtype, 'Point', 'x 1y')
            self.assertRaises(ValueError, recordtype, 'Point', 'x y x')
            self.assertRaises(ValueError, recordtype, 'Point', 'x y for')
            self.assertRaises(ValueError, recordtype, 'Point', '_field')
            self.assertRaises(ValueError, recordtype, 'Point', [('', 0)])
            self.assertRaises(ValueError, recordtype, '', 'x y')

        def test_bad_defaults(self):
            self.assertRaises(ValueError, recordtype, 'Point', [('x', 3, 4)])
            self.assertRaises(ValueError, recordtype, 'Point', [('x', )])
            self.assertRaises(ValueError, recordtype, 'Point', [3])

        def test_empty(self):
            Point = recordtype('Point', '')
            self.assertEqual(len(Point()), 0)
            self.assertEqual(list(Point()), [])
            self.assertEqual(Point(), Point())
            self.assertEqual(Point()._asdict(), {})
            Point = recordtype('Point', '', 10)
            self.assertEqual(len(Point()), 0)
            self.assertEqual(Point(), Point())
            self.assertEqual(Point()._asdict(), {})
            Point = recordtype('Point', [])
            self.assertEqual(len(Point()), 0)
            self.assertEqual(Point(), Point())
            self.assertEqual(Point()._asdict(), {})
            Point = recordtype('Point', [], 10)
            self.assertEqual(len(Point()), 0)
            self.assertEqual(Point(), Point())
            self.assertEqual(Point()._asdict(), {})

        def test_list(self):
            Point = recordtype('Point', ['x', 'y'])
            p = Point(10, 20)
            self.assertEqual((p.x, p.y), (10, 20))
            self.assertEqual(p._asdict(), {'x':10,  'y':20})
            Point = recordtype('Point', ('x', 'y'))
            p = Point(10, 20)
            self.assertEqual((p.x, p.y), (10, 20))
            self.assertEqual(p._asdict(), {'x':10,  'y':20})

        def test_default(self):
            Point = recordtype('Point', 'x y z', 100)
            self.assertEqual(Point(), Point(100, 100, 100))
            self.assertEqual(Point(10), Point(10, 100, 100))
            self.assertEqual(Point(10, 20), Point(10, 20, 100))
            self.assertEqual(Point(10, 20, 30), Point(10, 20, 30))
            self.assertEqual(Point()._asdict(), {'x':100,  'y':100,  'z':100})

        def test_default_list(self):
            Point = recordtype('Point', 'x y z'.split(), 100)
            self.assertEqual(Point(), Point(100, 100, 100))
            self.assertEqual(Point(10), Point(10, 100, 100))
            self.assertEqual(Point(10, 20), Point(10, 20, 100))
            self.assertEqual(Point(10, 20, 30), Point(10, 20, 30))
            self.assertEqual(Point()._asdict(), {'x':100,  'y':100,  'z':100})

        def test_default_and_specified_default(self):
            Point = recordtype('Point', ['x', ('y', 10), ('z', 20)], 100)
            self.assertEqual(Point(), Point(100, 10, 20))
            self.assertEqual(Point(0), Point(0, 10, 20))
            self.assertEqual(Point(0, 1), Point(0, 1, 20))
            self.assertEqual(Point(0, 1, 2), Point(0, 1, 2))
            Point = recordtype('Point', [('x', 0), 'y', ('z', 20)], 100)
            self.assertEqual(Point(), Point(0, 100, 20))

        def test_equality_inequality(self):
            Point = recordtype('Point', ['x', ('y', 10), ('z', 20)], 100)
            p0 = Point()
            p1 = Point(0)
            self.assertEqual(p0, Point())
            self.assertEqual(p0, Point(100, 10, 20))
            self.assertEqual(p1, Point(0, 10))
            self.assertEqual(Point(), p0)
            self.assertEqual(p0, p0)
            self.assertNotEqual(p0, p1)
            self.assertNotEqual(p0, 3)
            self.assertNotEqual(p0, None)
            self.assertNotEqual(p0, object())
            self.assertNotEqual(p0, Point('100'))

        def test_default_order(self):
            self.assertRaises(ValueError, recordtype, 'Point', ['x', ('y', 10), 'z'])
            Point = recordtype('Point', ['x', ('y', 10), 'z'], -1)
            self.assertEqual(Point(0), Point(0, 10, -1))
            self.assertEqual(Point(z=0), Point(-1, 10, 0))

        def test_repr(self):
            Point = recordtype('Point', 'x y z')
            p = Point(1, 2, 3)
            self.assertEqual(repr(p), 'Point(x=1, y=2, z=3)')
            self.assertEqual(str(p), 'Point(x=1, y=2, z=3)')

        def test_missing_argument(self):
            Point = recordtype('Point', ['x', 'y', ('z', 10)])
            self.assertEqual(Point(1, 2), Point(1, 2, 10))
            self.assertRaises(TypeError, Point, 1)

        def test_identity_of_defaults(self):
            default = object()
            Point = recordtype('Point', [('x', default)])
            self.assertTrue(Point().x is default)
            Point = recordtype('Point', 'x', default)
            self.assertTrue(Point().x is default)

        def test_writable(self):
            Point = recordtype('Point', ['x', ('y', 10), ('z', 20)], 100)
            p = Point(0)
            self.assertEqual((p.x, p.y, p.z), (0, 10, 20))
            p.x = -1
            self.assertEqual((p.x, p.y, p.z), (-1, 10, 20))
            p.y = -1
            self.assertEqual((p.x, p.y, p.z), (-1, -1, 20))
            p.z = None
            self.assertEqual((p.x, p.y, p.z), (-1, -1, None))

        def test_complex_defaults(self):
            Point = recordtype('Point', ['x', ('y', 10), ('z', 20)], [1, 2, 3])
            p = Point()
            self.assertEqual((p.x, p.y, p.z), ([1, 2, 3], 10, 20))
            Point = recordtype('Point', [('x', [4, 5, 6]), ('y', 10), ('z', 20)])
            p = Point()
            self.assertEqual((p.x, p.y, p.z), ([4, 5, 6], 10, 20))

        def test_iteration(self):
            Point = recordtype('Point', ['x', ('y', 10), ('z', 20)], [1, 2, 3])
            p = Point()
            self.assertEqual(len(p), 3)
            self.assertEqual(list(iter(p)), [[1, 2, 3], 10, 20])

        def test_fields(self):
            Point = recordtype('Point', 'x y z')
            self.assertEqual(Point._fields, ('x', 'y', 'z'))
            Point = recordtype('Point', 'x y z', 100)
            self.assertEqual(Point._fields, ('x', 'y', 'z'))
            Point = recordtype('Point', [('x', 0), ('y', 0), ('z', 0)])
            self.assertEqual(Point._fields, ('x', 'y', 'z'))

        def test_pickle(self):
            for p in (TestRT0(), TestRT(x=10, y=20, z=30)):
                for module in pickle_mods:
                    loads = getattr(module, 'loads')
                    dumps = getattr(module, 'dumps')
                    for protocol in (-1, 0, 1, 2):
                        q = loads(dumps(p, protocol))
                        self.assertEqual(p, q)
                        self.assertEqual(p._fields, q._fields)

        def test_type_has_same_name_as_field(self):
            Point = recordtype('Point', ['Point', ('y', 10), ('z', 20)], [1, 2, 3])
            p = Point()
            self.assertEqual(len(p), 3)
            self.assertEqual(p.Point, [1, 2, 3])
            Point = recordtype('Point', 'Point')
            p = Point(4)
            self.assertEqual(p.Point, 4)
            Point = recordtype('Point', 'x Point')
            p = Point(3, 4)
            self.assertEqual(p.Point, 4)

        def test_slots(self):
            Point = recordtype('Point', '')
            p = Point()
            self.assertRaises(AttributeError, setattr, p, 'x', 3)
            Point = recordtype('Point', '', use_slots=True)
            p = Point()
            self.assertRaises(AttributeError, setattr, p, 'x', 3)

        def test_no_slots(self):
            Point = recordtype('Point', '', use_slots=False)
            p = Point()
            p.x = 3

        def test_source(self):
            Point = recordtype('Point', '')
            self.assertTrue(hasattr(Point(), '_source'))

        def test_rename(self):
            Point = recordtype('Point', ('abc', 'def'), rename=True)
            self.assertEqual(Point._fields, ('abc', '_1'))
            Point = recordtype('Point', ('for', 'def'), rename=True)
            self.assertEqual(Point._fields, ('_0', '_1'))
            Point = recordtype('Point', 'a a b a b c', rename=True)
            self.assertEqual(Point._fields, ('a', '_1', 'b', '_3', '_4', 'c'))
            Point = recordtype('Point', 'x y z', rename=True)
            self.assertEqual(Point._fields, ('x', 'y', 'z'))
            Point = recordtype('Point', 'x y _z', rename=True)
            self.assertEqual(Point._fields, ('x', 'y', '_2'))
            Point = recordtype('Point', [('', 1), ('', 2)], rename=True)
            p = Point()
            self.assertEqual(p._0, 1)
            self.assertEqual(p._1, 2)

        def test_type_begins_with_underscore(self):
            Point = recordtype('_Point', '')
            p = Point()

        def test_mapping(self):
            Point = recordtype('Point', {'x':0,  'y':100})
            p = Point()
            self.assertEqual(p.x, 0)
            self.assertEqual(p.y, 100)

        def test_NO_DEFAULT(self):
            Point = recordtype('Point', {'x':0,  'y':NO_DEFAULT}, default=5)
            p = Point()
            self.assertEqual(p.x, 0)
            self.assertEqual(p.y, 5)

        def test_iterabale(self):
            Point = recordtype('Point', iter(['x', 'y']))
            p = Point(1, 2)
            self.assertEqual(p.x, 1)
            self.assertEqual(p.y, 2)

        def test_single_field(self):
            X = recordtype('X', 'xyz')
            self.assertEqual(X._fields, ('xyz', ))

        def test_repr_output(self):
            Point = recordtype('Point', 'a b')
            p = Point('0', 0)
            self.assertEqual(repr(p), "Point(a='0', b=0)")

        def test_mutable_defaults(self):
            A = recordtype('A', [('x', [])])
            a = A()
            self.assertEqual(a.x, [])
            a.x.append(4)
            self.assertEqual(a.x, [4])
            b = A()
            self.assertEqual(b.x, [4])


    unittest.main()
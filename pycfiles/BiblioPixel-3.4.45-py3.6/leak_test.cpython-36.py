# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/leak_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1169 bytes
import gc, sys, time, unittest, weakref
from bibliopixel import builder
from bibliopixel.project import project

class TestLeaks(unittest.TestCase):

    def test_leaks(self):

        def _get_items():
            items, stops = [], []
            for creator in _CREATORS:
                item, stop = creator()
                items.append(item)
                stops.append(stop)

            [stop() for stop in stops]
            return weakref.WeakSet(items)

        items = _get_items()
        _pause()
        self.assertEqual(list(items), [])


def _pause():
    time.sleep(0.1)


def _builder_simple():
    b = builder.Builder(shape=8, driver='dummy')
    b.start(True)
    _pause()
    return (b, b.stop)


def _builder_project():
    b, stop = _builder_simple()
    return (b.project, stop)


def _project_simple():
    desc = {'shape':8, 
     'driver':'dummy',  'run':{'threaded': True}}
    p = project.project(desc)
    p.start()
    _pause()
    return (p, p.stop)


_CREATORS = (
 _builder_simple, _builder_project, _project_simple)
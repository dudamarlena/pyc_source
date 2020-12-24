# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/messense/Projects/extender/tests/test_instancemanager.py
# Compiled at: 2014-06-12 00:09:11
import nose
from extender.manager import InstanceManager

class TestClass1(object):
    pass


class TestClass2(object):
    pass


def test_manager_with_not_instances():
    manager = InstanceManager(instances=False)
    manager.add(('{module}.{name}').format(module=TestClass1.__module__, name=TestClass1.__name__))
    manager.add(('{module}.{name}').format(module=TestClass2.__module__, name=TestClass2.__name__))
    manager.add('non.exists')
    classes = manager.all()
    assert len(classes) == 2


if __name__ == '__main__':
    nose.runmodule()
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uli/WorkShop/devel/zope/zope.pytest/tags/0.1/src/zope/pytest/tests/sample_fixtures/zcml/mypkg2/tests/test_app.py
# Compiled at: 2011-03-05 10:41:26
from zope.interface.verify import verifyClass, verifyObject
from mypkg2.app import SampleApp
from mypkg2.interfaces import ISampleApp

def test_app_create():
    app = SampleApp()
    assert app is not None
    return


def test_app_class_iface():
    assert verifyClass(ISampleApp, SampleApp)


def test_app_instance_iface():
    assert verifyObject(ISampleApp, SampleApp())
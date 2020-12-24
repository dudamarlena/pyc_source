# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/cloudservers/tests/test_images.py
# Compiled at: 2010-08-16 13:12:09
from cloudservers import Image
from fakeserver import FakeServer
from utils import assert_isinstance
from nose.tools import assert_equal
cs = FakeServer()

def test_list_images():
    il = cs.images.list()
    cs.assert_called('GET', '/images/detail')
    [ assert_isinstance(i, Image) for i in il ]


def test_get_image_details():
    i = cs.images.get(1)
    cs.assert_called('GET', '/images/1')
    assert_isinstance(i, Image)
    assert_equal(i.id, 1)
    assert_equal(i.name, 'CentOS 5.2')


def test_create_image():
    i = cs.images.create(server=1234, name='Just in case')
    cs.assert_called('POST', '/images')
    assert_isinstance(i, Image)


def test_delete_image():
    cs.images.delete(1)
    cs.assert_called('DELETE', '/images/1')


def test_find():
    i = cs.images.find(name='CentOS 5.2')
    assert_equal(i.id, 1)
    cs.assert_called('GET', '/images/detail')
    iml = cs.images.findall(status='SAVING')
    assert_equal(len(iml), 1)
    assert_equal(iml[0].name, 'My Server Backup')
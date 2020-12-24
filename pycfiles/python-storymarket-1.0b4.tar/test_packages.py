# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/python-storymarket/tests/test_packages.py
# Compiled at: 2010-09-13 15:44:42
from __future__ import absolute_import
from storymarket import Package, Audio, Data, Photo, Text, Video
from .fakeserver import FakeStorymarket
from .utils import assert_list_api, assert_get_api, assert_create_api, assert_isinstance
sm = FakeStorymarket()

def test_list_packages():
    assert_list_api(sm, sm.packages.all, Package, 'content/package/')


def test_get_package():
    assert_get_api(sm, sm.packages.get, Package, 'content/package/1/')


def test_related_resource_properties():
    test_data = [
     (
      'audio_items', Audio),
     (
      'data_items', Data),
     (
      'photo_items', Photo),
     (
      'text_items', Text),
     (
      'video_items', Video)]
    package = sm.packages.get(1)

    def check_related_resource_property(attname, cls):
        related = getattr(package, attname)
        assert_isinstance(related, list)
        assert_isinstance(related[0], cls)

    for (attname, cls) in test_data:
        yield (check_related_resource_property, attname, cls)


def test_post_packages():
    data = {'title': 'Test Package', 
       'org': sm.orgs.get(1), 
       'category': '/content/sub_category/1/', 
       'text_items': [
                    '/content/text/1/'], 
       'video_items': [
                     sm.video.get(1)], 
       'data_items': [
                    1]}
    assert_create_api(sm, sm.packages.create, sm.packages.get(1), data, 'content/package/')
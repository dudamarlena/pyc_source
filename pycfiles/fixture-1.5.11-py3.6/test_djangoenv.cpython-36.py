# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/test/test_loadable/test_django/test_djangoenv.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 1444 bytes
from blog.models import Post
from nose.tools import raises, assert_equal
from fixture import DataSet
from fixture.exc import StorageMediaNotFound
from fixture.loadable.django_loadable import DjangoEnv, DjangoFixture
from fixture.style import NamedDataStyle

@raises(ValueError)
def test_unsplittable_name():
    DjangoEnv.get('blog_Post')


def test_invalid_app_returns_none():
    assert_equal(None, DjangoEnv.get('no_such_app__Post'))


def test_invalid_model_returns_none():
    assert_equal(None, DjangoEnv.get('blog__NoSuchModel'))


def test_model_lookup_by_qualified_model_name():

    class SomeDataset(DataSet):

        class Meta:
            django_model = 'blog.Post'

        class foo:
            foo = 1

    fixture = DjangoFixture()
    ds = SomeDataset()
    fixture.attach_storage_medium(ds)
    assert_equal(ds.meta.storage_medium.medium, Post)


@raises(ValueError)
def test_dataset_with_malformed_model_name():

    class SomeDataset(DataSet):

        class Meta:
            django_model = 'not_dot_separated_model_name'

        class foo:
            foo = 1

    fixture = DjangoFixture()
    ds = SomeDataset()
    fixture.attach_storage_medium(ds)


@raises(StorageMediaNotFound)
def test_dataset_without_resolvable_model_name():

    class UnknownData(DataSet):

        class foo:
            foo = 1

    fixture = DjangoFixture(style=(NamedDataStyle()))
    ds = UnknownData()
    fixture.attach_storage_medium(ds)
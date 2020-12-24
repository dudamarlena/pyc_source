# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/test/test_loadable/test_django/test_loading.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 1451 bytes
from app.models import Author, Book, Reviewer
from fixture import DjangoFixture
from fixture.test.test_loadable.test_django.util import assert_empty
from fixture.test.test_loadable.test_django.fixtures import DjangoDataSetWithMeta, AuthorData, BookData, ReviewerData
dj_fixture = DjangoFixture()

def test_fk_rels():
    assert_empty('app')
    try:
        data = dj_fixture.data(AuthorData, BookData)
        data.setup()
        assert Author.objects.get(first_name='Frank').books.count() == 1
    finally:
        data.teardown()

    assert_empty('app')


def test_m2m():
    assert_empty('app')
    try:
        data = dj_fixture.data(AuthorData, BookData, ReviewerData)
        data.setup()
        ben = Reviewer.objects.all()[0]
        assert ben.reviewed.count() == 2
        dune = Book.objects.get(title='Dune')
        assert ben in dune.reviewers.all()
        frank = Author.objects.get(first_name='Frank')
        assert frank.books.count() == 1
        assert dune in frank.books.all()
    finally:
        data.teardown()

    assert_empty('app')


def test_dataset_with_meta():
    assert_empty('app')
    try:
        data = dj_fixture.data(DjangoDataSetWithMeta)
        data.setup()
        assert Author.objects.count() == 2
    finally:
        data.teardown()

    assert_empty('app')
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/test/test_loadable/test_django/test_wrong_declarations.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 1181 bytes
from nose.tools import assert_raises
from fixture.test.test_loadable.test_django.util import assert_empty
from fixture import DjangoFixture, DataSet, style
from app import models
from fixture.exc import LoadError

class ReviewerData(DataSet):

    class ben:
        name = 'ben'


class BookData(DataSet):

    class dune:
        title = 'Dune'
        reviewers = [ReviewerData.ben]


class AuthorData(DataSet):

    class frank_herbert:
        first_name = 'Frank'
        last_name = 'Herbert'
        books = BookData.dune


dj_fixture = DjangoFixture(env=models, style=(style.NamedDataStyle()))

def test_wrong_relation_declaration():
    assert_empty('app')
    assert 'reviewers' in {f.name for f in models.Book._meta.get_fields()}
    data = dj_fixture.data(BookData)
    assert_raises(LoadError, data.setup)
    data.teardown()
    assert_empty('app')


def test_invalid_m2m():

    class ReviewerData(DataSet):

        class ben:
            name = 'ben'
            reviewed = [BookData.dune, AuthorData.frank_herbert]

    assert_empty('app')
    data = dj_fixture.data(ReviewerData)
    assert_raises(LoadError, data.setup)
    data.teardown()
    assert_empty('app')
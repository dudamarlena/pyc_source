# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/test/test_loadable/test_django/fixtures.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 1248 bytes
from fixture import DataSet

class ValidNoRelationsData(DataSet):

    class one:
        char = 'one'
        num = 1

    class two:
        char = 'two'
        num = 2


class InvalidNoRelationsData(DataSet):

    class one:
        char = 'one'
        invalid = 'test'

    class two:
        char = 'two'
        some_other = 2


class AuthorData(DataSet):

    class Meta:
        django_model = 'app.Author'

    class frank_herbert:
        first_name = 'Frank'
        last_name = 'Herbert'

    class guido:
        first_name = 'Guido'
        last_name = 'Van rossum'


class BookData(DataSet):

    class Meta:
        django_model = 'app.Book'

    class dune:
        title = 'Dune'
        author = AuthorData.frank_herbert

    class python:
        title = 'Python'
        author = AuthorData.guido


class ReviewerData(DataSet):

    class Meta:
        django_model = 'app.Reviewer'

    class ben:
        name = 'ben'
        reviewed = [BookData.dune, BookData.python]


class DjangoDataSetWithMeta(DataSet):

    class Meta:
        django_model = 'app.Author'

    class frank_herbert:
        first_name = 'Frank'
        last_name = 'Herbert'

    class guido:
        first_name = 'Guido'
        last_name = 'Van rossum'
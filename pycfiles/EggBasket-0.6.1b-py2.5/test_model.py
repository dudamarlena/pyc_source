# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eggbasket/tests/test_model.py
# Compiled at: 2008-07-13 16:55:56
"""Unit test cases for testing you application's model classes.

If your project uses a database, you should set up database tests similar to
what you see below.

Be sure to set the ``db_uri`` in the ``test.cfg`` configuration file in the
top-level directory of your project to an appropriate uri for your testing
database. SQLite is a good choice for testing, because you can use an in-memory
database which is very fast and the data in it has to be boot-strapped from
scratch every time, so the tests are independant of any pre-existing data.

You can also set the ``db_uri``directly in this test file but then be sure
to do this before you import your model, e.g.::

    from turbogears import testutil, database
    database.set_db_uri("sqlite:///:memory:")
    from eggbasket.model import YourModelClass, User, ...
"""
from turbogears import testutil, database
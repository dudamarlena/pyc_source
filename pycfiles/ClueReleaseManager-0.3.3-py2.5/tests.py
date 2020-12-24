# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/clue/relmgr/tests.py
# Compiled at: 2009-09-18 12:06:12
import os, unittest, doctest, logging
from clue.relmgr import utils
import sqlalchemy as sa
from sqlalchemy import orm
import tempfile

def setup_sql(test):
    from clue.relmgr.model import metadata
    (unused, tmpfile) = tempfile.mkstemp()
    engine = sa.create_engine('sqlite:///' + tmpfile)
    metadata.create_all(engine)
    sessionmaker = orm.sessionmaker(bind=engine)
    test.globs['sessionmaker'] = sessionmaker
    test.globs['dbfile'] = tmpfile


def teardown_sql(test):
    os.remove(test.globs['dbfile'])


def test_suite():
    logging.basicConfig()
    utils.logger.setLevel(logging.ERROR)
    flags = doctest.ELLIPSIS
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite('clue.relmgr.model', setUp=setup_sql, tearDown=teardown_sql, optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.relmgr.cmdtool', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.relmgr.pypi', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.relmgr.wsgiapp', optionflags=flags))
    return suite


def main():
    runner = unittest.TextTestRunner()
    runner.run(test_suite())


if __name__ == '__main__':
    main()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_software_collections_list.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import software_collections_list as parsermodule
from insights.parsers.software_collections_list import SoftwareCollectionsListInstalled
from insights.tests import context_wrap
from doctest import testmod
EXAMPLE_IN_DOCS = '\ndevtoolset-7\nhttpd24\npython27\nrh-mysql57\nrh-nodejs8\nrh-php71\nrh-python36\nrh-ruby24\n'
EXAMPLE_WITH_EMPTY_LINES = '\ndevtoolset-7\nhttpd24\n\npython27\nrh-mysql57\n\nrh-nodejs8\nrh-php71\nrh-python36\n\nrh-ruby24\n'
EXAMPLE_WITH_SPACES = '\n        devtoolset-7  \t\nhttpd24\npython27   \t\nrh-mysql57   \t\n  rh-nodejs8  \t\nrh-php71\nrh-python36\nrh-ruby24   \n\n'
EXAMPLE_EMPTY = ''
COLLECTIONS_LIST = [
 'devtoolset-7',
 'httpd24',
 'python27',
 'rh-mysql57',
 'rh-nodejs8',
 'rh-php71',
 'rh-python36',
 'rh-ruby24']

def _assert_collections(coll_parser, coll_list):
    assert coll_parser.records == coll_list
    for coll in coll_list:
        assert coll_parser.exists(coll)


def test_module_documentation():
    failed, total = testmod(parsermodule, globs={'collections': SoftwareCollectionsListInstalled(context_wrap(EXAMPLE_IN_DOCS))})
    assert failed == 0


def test_swcol_parsing():
    scls = SoftwareCollectionsListInstalled(context_wrap(EXAMPLE_IN_DOCS))
    _assert_collections(scls, COLLECTIONS_LIST)


def test_swcol_exceptions_in_input():
    scls = SoftwareCollectionsListInstalled(context_wrap(EXAMPLE_WITH_EMPTY_LINES))
    _assert_collections(scls, COLLECTIONS_LIST)
    assert not scls.exists('foo')
    scls = SoftwareCollectionsListInstalled(context_wrap(EXAMPLE_WITH_SPACES))
    _assert_collections(scls, COLLECTIONS_LIST)
    assert not scls.exists('bar')
    scls = SoftwareCollectionsListInstalled(context_wrap(EXAMPLE_EMPTY))
    _assert_collections(scls, [])
    assert not scls.exists('rh-joke')
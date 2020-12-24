# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_predicates.py
# Compiled at: 2014-05-04 12:45:31
__doc__ = 'Route predicate related tests.'
import pytest
from pyramid_localize.routing.predicates import language

@pytest.mark.parametrize('match_info, matched', (
 ({'match': {'_LOCALE_': 'en'}},
  True),
 ({'match': {'_LOCALE_': 'fr'}},
  False),
 ({'match': {}},
  False)))
def test_predicate(web_request, match_info, matched):
    """Test matches according to web_request config."""
    predicate = language('_LOCALE_')
    assert predicate(match_info, web_request) == matched
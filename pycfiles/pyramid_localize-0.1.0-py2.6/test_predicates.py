# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_predicates.py
# Compiled at: 2014-05-04 12:45:31
"""Route predicate related tests."""
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
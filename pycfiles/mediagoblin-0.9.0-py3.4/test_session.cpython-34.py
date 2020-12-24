# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_session.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 1109 bytes
from mediagoblin.tools import session

def test_session():
    sess = session.Session()
    assert not sess
    assert not sess.is_updated()
    sess['user_id'] = 27
    assert sess
    assert not sess.is_updated()
    sess.save()
    assert sess.is_updated()
    sess.delete()
    assert not sess
    assert sess.is_updated()
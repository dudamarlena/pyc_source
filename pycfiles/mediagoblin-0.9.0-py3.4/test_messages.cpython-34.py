# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_messages.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 2108 bytes
from mediagoblin import messages
from mediagoblin.tools import template

def test_messages(test_app):
    """
    Added messages should show up in the request.session,
    fetched messages should be the same as the added ones,
    and fetching should clear the message list.
    """
    test_app.get('/')
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/root.html']
    request = context['request']
    assert request.session.get('messages', []) == []
    messages.clear_add_message()
    messages.add_message(request, 'herp_derp', 'First!')
    test_msg_queue = [{'text': 'First!',  'level': 'herp_derp'}]
    assert messages.ADD_MESSAGE_TEST[(-1)] == test_msg_queue
    assert messages.ADD_MESSAGE_TEST[(-1)] == request.session['messages']
    assert messages.fetch_messages(request) == test_msg_queue
    assert request.session.get('messages') == []
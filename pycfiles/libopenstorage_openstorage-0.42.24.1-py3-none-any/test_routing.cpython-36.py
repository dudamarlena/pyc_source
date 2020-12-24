# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/jeepney/jeepney/tests/test_routing.py
# Compiled at: 2020-01-10 16:25:36
# Size of source mod 2**32: 959 bytes
from asyncio import Future
import pytest
from jeepney.routing import Router
from jeepney.wrappers import new_method_return, new_error, DBusErrorResponse
from jeepney.bus_messages import message_bus

def test_message_reply():
    router = Router(Future)
    call = message_bus.Hello()
    future = router.outgoing(call)
    router.incoming(new_method_return(call, 's', ('test', )))
    assert future.result() == ('test', )


def test_error():
    router = Router(Future)
    call = message_bus.Hello()
    future = router.outgoing(call)
    router.incoming(new_error(call, 'TestError', 'u', (31, )))
    with pytest.raises(DBusErrorResponse) as (e):
        future.result()
    if not e.value.name == 'TestError':
        raise AssertionError
    elif not e.value.data == (31, ):
        raise AssertionError


def test_unhandled():
    unhandled = []
    router = Router(Future, on_unhandled=(unhandled.append))
    msg = message_bus.Hello()
    router.incoming(msg)
    if not len(unhandled) == 1:
        raise AssertionError
    elif not unhandled[0] == msg:
        raise AssertionError
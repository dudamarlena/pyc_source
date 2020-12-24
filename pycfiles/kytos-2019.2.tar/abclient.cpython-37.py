# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/humberto/src/kytos/kytos-asyncio/kytos/core/abclient.py
# Compiled at: 2018-09-06 11:53:18
# Size of source mod 2**32: 5244 bytes
"""
Autobahn client to publish Kytos events as WAMP messages.

Connects to a crossbar.io router and publishes all messages from the new UI
event buffer.

Event flow:

  app event -> ui event -> ui buffer
                             |
                             |
                             V
                      autobahn client
                             |
                             |
                             V
                      crossbar router
                       (kytos realm)
                             |
                             |
                             V
                       any wamp client

Instructions on how to run:

1. Checkout kytos' "autobahn" branch

2. Run kytosd:

  $ kytosd -f

3. Start crossbar router from docker

  $ docker run --user 1000 -v ${PWD}:/node -p 8080:8080 --name crossbar --rm -it crossbario/crossbar --colour true

4. That starts a local autobahn web client where events are published:

  http://localhost:8080

"""
from autobahn.asyncio.component import Component, run
from autobahn.wamp.types import SubscribeOptions, PublishOptions
import asyncio, txaio
LOG = txaio.make_logger()
component = Component(transports='ws://localhost:8080/ws',
  realm='kytos')

def on_event(name, content, source):
    msg = f"'{name}' event, content: {content}, source: {source}"
    print(msg)


def on_ping(counter, content, source):
    msg = f"ui.ping event #{counter}, content: {content}, source: {source}"
    LOG.info(msg)


@component.on_join
async def joined(session, details):
    LOG.info('session ready')
    if not getattr(component, 'session', None):
        component.session = session
    match_prefix = SubscribeOptions(match='prefix')
    await session.subscribe(on_ping, 'kytos/ui.ping')
    await session.subscribe(on_event, 'kytos/core.', match_prefix)
    await session.subscribe(on_event, 'kytos/of_core.', match_prefix)
    await session.subscribe(on_event, 'kytos/topology.', match_prefix)
    loop = asyncio.get_event_loop()
    loop.create_task(core_ping())
    loop.create_task(ui_event_handler())


async def ui_event_handler():
    """
    Watches the `ui_buffer` event queue to forward its events to WAMP channels.

    """
    LOG.info('Starting UI event handler')
    while 1:
        event = await component.ui_buffer.aget()
        serialized_content = serialize_dict(event.content)
        print(f"Forwarding new UI event received from Kytos: {event}, content: {serialized_content}")
        component.session.publish(topic=(event.name), name=(event.name),
          content=serialized_content,
          source='kytos.core.abclient',
          options=PublishOptions(exclude_me=False))
        if event.name == 'kytos/core.shutdown':
            LOG.debug('App Event handler stopped')
            break


async def core_ping():
    """
    Generate ping event to ease event tests.
    """
    counter = 0
    while True:
        component.session.publish(topic='kytos/ui.ping', name='kytos/ui.ping',
          content=counter,
          source='kytos.core.abclient',
          options=PublishOptions(exclude_me=false))
        counter += 1
        await asyncio.sleep(2)


def serialize_dict(data: dict):
    """Force conversion of value objects to JSON.

    If we don't make this conversion manually, autobahn.wamp.serializer
    will cause this exception:

    umsgpack.UnsupportedTypeException:
      unsupported type: <class 'kytos.core.switch.Switch'>
    """
    result = {}
    for key, obj in data.items():
        if not isinstance(obj, str):
            if getattr(obj, 'as_json', None):
                obj = obj.as_json()
            else:
                if callable(obj):
                    continue
                else:
                    if isinstance(obj, dict):
                        obj = serialize_dict(obj)
                    else:
                        print("XXX key '%s' doesn't have .as_json(), value: %s, class %s" % (key, obj, type(obj)))
                        obj = str(obj)
        result[key] = obj

    return result


if __name__ == '__main__':
    run([component])
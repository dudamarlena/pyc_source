# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/humberto/src/kytos/kytos-asyncio/kytos/core/helpers.py
# Compiled at: 2019-06-06 13:59:39
# Size of source mod 2**32: 4431 bytes
"""Utilities functions used in Kytos."""
from datetime import datetime, timezone
from threading import Thread
from kytos.core.napps import rest
__all__ = [
 'listen_to', 'now', 'rest', 'run_on_thread', 'get_time']

def listen_to(event, *events):
    """Decorate Event Listener methods.

    This decorator was built to be used on NAPPs methods to define which
    type of event the method will handle. With this, we will be able to
    'schedule' the app/method to receive an event when a new event is
    registered on the controller buffers.
    By using the run_on_thread decorator, we also guarantee that the method
    (handler) will be called from inside a new thread, avoiding this method to
    block its caller.

    The decorator will add an attribute to the method called 'events', that
    will be a list of the events that the method will handle.

    The event that will be listened to is always a string, but it can represent
    a regular expression to match against multiple Event Types. All listened
    events are documented in :doc:`/developer/listened_events` section.

    Example of usage:

    .. code-block:: python3

        class MyAppClass(KytosApp):
            @listen_to('kytos/of_core.messages.in')
            def my_handler_of_message_in(self, event):
                # Do stuff here...

            @listen_to('kytos/of_core.messages.out')
            def my_handler_of_message_out(self, event):
                # Do stuff here...

            @listen_to('kytos/of_core.messages.in.ofpt_hello',
                       'kytos/of_core.messages.out.ofpt_hello')
            def my_handler_of_hello_messages(self, event):
                # Do stuff here...

            @listen_to('kytos/of_core.message.*.hello')
            def my_other_handler_of_hello_messages(self, event):
                # Do stuff here...

            @listen_to('kytos/of_core.message.*.hello')
            def my_handler_of_hello_messages(self, event):
                # Do stuff here...

            @listen_to('kytos/of_core.message.*')
            def my_stats_handler_of_any_message(self, event):
                # Do stuff here...
    """

    def decorator(handler):

        @run_on_thread
        def threaded_handler(*args):
            handler(*args)

        threaded_handler.events = [
         event]
        threaded_handler.events.extend(events)
        return threaded_handler

    return decorator


def now(tzone=timezone.utc):
    """Return the current datetime (default to UTC).

    Args:
        tzone (datetime.timezone): Specific time zone used in datetime.

    Returns:
        datetime.datetime.now: Date time with specific time zone.

    """
    return datetime.now(tzone)


def run_on_thread(method):
    """Decorate to run the decorated method inside a new thread.

    Args:
        method (function): function used to run as a new thread.

    Returns:
        Decorated method that will run inside a new thread.
        When the decorated method is called, it will not return the created
        thread to the caller.

    """

    def threaded_method(*args):
        thread = Thread(target=method, args=args)
        thread.daemon = True
        thread.start()

    return threaded_method


def get_time(data=None):
    """Receive a dictionary or a string and return a datatime instance.

    data = {"year": 2006,
            "month": 11,
            "day": 21,
            "hour": 16,
            "minute": 30 ,
            "second": 00}

    or

    data = "21/11/06 16:30:00"

    2018-04-17T17:13:50Z

    Args:
        data (str, dict): python dict or string to be converted to datetime

    Returns:
        datetime: datetime instance.

    """
    if isinstance(data, str):
        date = datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
    else:
        if isinstance(data, dict):
            date = datetime(**data)
        else:
            return
    return date.replace(tzinfo=(timezone.utc))
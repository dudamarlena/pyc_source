# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/um/background_messages.py
# Compiled at: 2018-12-13 14:13:37
# Size of source mod 2**32: 3612 bytes
from django.core.cache import cache
from django.contrib.messages import constants, add_message

def message_user(user, message, level=constants.INFO):
    """Send a message to a particular user.

    A list of messages is stored in the cache to allow having multiple messages
    queued up for a user. This non-atomic read-modify-write makes it possible
    to lose messages under concurrency.

    :param user: User instance
    :param message: Message to show
    :param level: Message level
    """
    if user.id is None:
        raise ValueError('Anonymous users cannot send messages')
    user_key = _user_key(user)
    messages = cache.get(user_key) or []
    messages.append((message, level))
    cache.set(user_key, messages)


def _get_messages(user):
    """Fetch messages for given user.

    :param user: User instance
    """
    if user.id is None:
        return []
    else:
        key = _user_key(user)
        result = cache.get(key)
        if result:
            cache.delete(key)
            return result
        return []


def add_background_messages_to_contrib_messages(request):
    """Merge background messages with normal contrib.message."""
    for msg, level in _get_messages(request.user):
        add_message(request, level, msg)


def _user_key(user):
    if isinstance(user, int):
        return '_async_message_%d' % user
    else:
        return '_async_message_%d' % user.pk


def debug(user, message):
    """
    Adds a message with the ``DEBUG`` level.

    :param user: User instance
    :param message: Message to show
    """
    message_user(user, message, constants.DEBUG)


def info(user, message):
    """
    Adds a message with the ``INFO`` level.

    :param user: User instance
    :param message: Message to show
    """
    message_user(user, message, constants.INFO)


def success(user, message):
    """
    Adds a message with the ``SUCCESS`` level.

    :param user: User instance
    :param message: Message to show
    """
    message_user(user, message, constants.SUCCESS)


def warning(user, message):
    """
    Adds a message with the ``WARNING`` level.

    :param user: User instance
    :param message: Message to show
    """
    message_user(user, message, constants.WARNING)


def error(user, message):
    """
    Adds a message with the ``ERROR`` level.

    :param user: User instance
    :param message: Message to show
    """
    message_user(user, message, constants.ERROR)
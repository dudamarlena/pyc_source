# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/discordaio/webhook.py
# Compiled at: 2018-02-25 13:02:06
# Size of source mod 2**32: 1124 bytes
"""Webhooks are a low-effort way to post messages to channels in Discord. They do not require a bot user or authentication to use."""
from .base import DiscordObject

class Webhook(DiscordObject):
    __doc__ = 'Used to represent a webhook.\n\n    .. versionadded:: 0.2.0\n\n    Attributes:\n        id (:obj:`int`): the id of the webhook\n        guild_id (:obj:`int`, optional): the guild id this webhook is for\n        channel_id (:obj:`int`): the channel id this webhook is for\n        user (:class:`.User`): the user this webhook was created by (not returned when getting a webhook with its token)\n        name (:obj:`str`): the default name of the webhook\n        avatar (:obj:`str`): the default avatar of the webhook\n        token (:obj:`str`): the secure token of the webhook\n    '

    def __init__(self, id=0, guild_id=0, channel_id=0, user=None, name='', avatar='', token=''):
        self.id = id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.user = user
        self.name = name
        self.avatar = avatar
        self.token = token


__all__ = [
 'Webhook']
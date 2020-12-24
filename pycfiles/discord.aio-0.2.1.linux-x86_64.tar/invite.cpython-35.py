# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/discordaio/invite.py
# Compiled at: 2018-02-25 13:02:06
# Size of source mod 2**32: 2169 bytes
from .base import DiscordObject
from .guild import Guild
from .channel import Channel
from .user import User

class Invite(DiscordObject):
    __doc__ = 'Represents a code that when used, adds a user to a guild.\n\n    .. versionadded:: 0.2.0\n\n    Attributes:\n        code (:obj:`str`): the invite code (unique ID)\n        guild (:class:`.Guild`): the guild this invite is for\n        channel (:class:`.Channel`): the channel this invite is for\n    '

    def __init__(self, code='', guild=None, channel=None):
        self.code = code
        self.guild = guild
        self.channel = channel

    async def _from_api_ext(self, key, value):
        if key == 'guild':
            setattr(self, key, await Guild.from_api_res(value))
        else:
            if key == 'channel':
                setattr(self, key, await Channel.from_api_res(value))
            else:
                return await super()._from_api_ext(key, value)


class InviteMetadata(DiscordObject):
    __doc__ = 'Represents the invite metadata\n\n    .. versionadded:: 0.2.0\n\n    Attributes:\n        inviter (:class:`.A`): user object user who created the invite\n        uses (:obj:`int`): number of times this invite has been used\n        max_uses (:obj:`int`): max number of times this invite can be used\n        max_age (:obj:`int`): duration (in seconds) after which the invite expires\n        temporary (:obj:`bool`): whether this invite only grants temporary membership\n        created_at (:obj:`int`): timestamp when this invite was created\n        revoked (:obj:`bool`): whether this invite is revoked\n    '

    def __init__(self, inviter=None, uses=0, max_uses=0, max_age=0, temporary=False, created_at=None, revoked=False):
        self.inviter = inviter
        self.uses = uses
        self.max_uses = max_uses
        self.max_age = max_age
        self.temporary = temporary
        self.created_at = created_at
        self.revoked = revoked

    async def _from_api_ext(self, key, value):
        if key == 'inviter':
            setattr(self, key, await User.from_api_res(value))
        else:
            return await super()._from_api_ext(key, value)


__all__ = [
 'Invite',
 'InviteMetadata']
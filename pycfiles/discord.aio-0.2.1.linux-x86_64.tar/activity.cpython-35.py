# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/discordaio/activity.py
# Compiled at: 2018-02-25 13:02:06
# Size of source mod 2**32: 3342 bytes
from .base import DiscordObject

class ActivityParty(DiscordObject):
    __doc__ = "Activity party\n\n    .. versionadded:: 0.2.0\n\n    Attributes:\n        id (:obj:`str`, optional): the id of the party\n        size (:obj:`list` of :obj:`int`): array of two integers (current_size, max_size), used to show the party's current and maximum size\n    "

    def __init__(self, id='', size=[]):
        self.id = id
        self.size = size


class ActivityTimestamps(DiscordObject):
    __doc__ = 'Activity timestamps\n\n    .. versionadded:: 0.2.0\n\n    Attributes:\n        start (:obj:`int`, optional): unix time (in milliseconds) of when the activity started\n        end (:obj:`int`, optional): unix time (in milliseconds) of when the activity ends\n    '

    def __init__(self, start=0, end=0):
        self.start = start
        self.end = end


class ActivityAssets(DiscordObject):
    __doc__ = 'Activity assets\n\n    .. versionadded:: 0.2.0\n\n    Attributes:\n        large_image (:obj:`str`, optional): the id for a large asset of the activity, usually a snowflake\n        large_text (:obj:`str`, optional): text displayed when hovering over the large image of the activity\n        small_image (:obj:`str`, optional): the id for a small asset of the activity, usually a snowflake\n        small_text (:obj:`str`, optional): text displayed when hovering over the small image of the activity\n    '

    def __init__(self, large_image='', large_text='', small_image='', small_text=''):
        self.large_image = large_image
        self.large_text = large_text
        self.small_image = small_image
        self.small_text = small_text


class Activity(DiscordObject):
    __doc__ = "Represents a discord activity\n\n    .. versionadded:: 0.2.0\n\n    Attributes:\n        name (:obj:`str`): the activity's name\n        type (:obj:`int`): activity type\n        url (:obj:`str`, optional): stream url, is validated when type is 1\n        timestamps (:class:`.Timestamps`): object unix timestamps for start and/or end of the game\n        application_id (:obj:`int`, optional): application id for the game\n        details (:obj:`str`, optional): what the player is currently doing\n        state (:obj:`str`, optional): the user's current party status\n        party (:class:`.Party`): object information for the current party of the player\n        assets (:class:`.Assets`): object images for the presence and their hover texts\n    "

    def __init__(self, name='', type=0, url='', timestamps=None, application_id=0, details='', state='', party=None, assets=None):
        self.name = name
        self.type = type
        self.url = url
        self.timestamps = timestamps
        self.application_id = application_id
        self.details = details
        self.state = state
        self.party = party
        self.assets = assets

    async def _from_api_ext(self, key, value):
        if key == 'timestamps':
            setattr(self, key, await ActivityTimestamps.from_api_res(value))
        else:
            if key == 'party':
                setattr(self, key, await ActivityParty.from_api_res(value))
            else:
                if key == 'assets':
                    setattr(self, key, await ActivityAssets.from_api_res(value))
                else:
                    await super()._from_api_ext(key, value)


__all__ = ['Activity',
 'ActivityParty',
 'ActivityTimestamps',
 'ActivityAssets']
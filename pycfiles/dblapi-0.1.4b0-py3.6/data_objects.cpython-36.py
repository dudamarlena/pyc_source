# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dblapi\data_objects.py
# Compiled at: 2018-04-08 07:11:21
# Size of source mod 2**32: 10301 bytes
import dateutil.parser
from .errors import *
VALID_STATIC_FORMATS = {
 'jpeg', 'jpg', 'webp', 'png'}
VALID_AVATAR_FORMATS = VALID_STATIC_FORMATS | {'gif'}

class Avatar:
    __doc__ = "\n    Avatar object for easy to use interface. Get url by simply using :any:`url` method.\n    If called as a string outputs .png url. You can get .gif if you use :any:`gif` method and\n    you can resize image by using :any:`size` method.\n\n    .. container:: operations\n\n        .. describe:: x == y\n\n            Checks if two users are equal.\n\n        .. describe:: x != y\n\n            Checks if two users are not equal.\n\n        .. describe:: hash(x)\n\n            Return the user's hash.\n\n        .. describe:: str(x)\n\n            Returns the user's name with discriminator.\n\n    Parameters\n    -----------\n    img_hash: :class:`str`\n        Avatar hash from discord.\n    bot_id: :class:`int`\n        Bot Client ID\n\n    Attributes\n    -----------\n    hash: :class:`str`\n        Avatar hash\n    base_url: :class:`str`\n        Base URL for avatar image without file suffix.\n    default_avatar_url: :class:`str`\n        Returns URL of default avatar.\n    "

    def __init__(self, img_hash, bot_id: int):
        """

        :param img_hash:
        :param bot_id:
        """
        self.hash = str(img_hash)
        self.base_url = f"https://cdn.discordapp.com/avatars/{bot_id}/{self.hash}"
        self.default_avatar_url = f"https://cdn.discordapp.com/embed/avatars/{bot_id % 5}.png"

    @property
    def url(self):
        """
        Returns URL of bots/users avatar.

        :return: :class:`str`
            URL of the .webp if avatar is not animated or .gif avatar is animated.
        """
        return self.url_as()

    @property
    def is_avatar_animated(self) -> bool:
        """
        Returns True if avatar is animated, False otherwise.

        :return: :class:`bool`
        """
        return self.hash.startswith('a_')

    def url_as(self, format: str=None, static_format: str='webp', size: int=1024) -> str:
        if not (size != 0 and not size & size - 1):
            if size in range(16, 1025):
                raise InvalidArgument('size must be a power of 2 between 16 and 1024')
            if format is not None:
                if format not in VALID_AVATAR_FORMATS:
                    raise InvalidArgument('format must be None or one of {}'.format(VALID_AVATAR_FORMATS))
        else:
            if format == 'gif':
                if not self.is_avatar_animated:
                    raise InvalidArgument('non animated avatars do not support gif format')
            if static_format not in VALID_STATIC_FORMATS:
                raise InvalidArgument('static_format must be one of {}'.format(VALID_STATIC_FORMATS))
        if self.hash is None:
            return self.default_avatar_url
        else:
            if format is None:
                if self.is_avatar_animated:
                    format = 'gif'
                else:
                    format = static_format
            gif_fix = '&_=.gif' if format == 'gif' else ''
            return '{0.base_url}.{1}?size={2}{3}'.format(self, format, size, gif_fix)

    def __str__(self):
        """
        Same as :any:`url`. Returns .png URL of bots/users avatar.

        :return: :class:`str`
            URL of the .png avatar image.
        """
        return self.base_url + '.png'

    def __get__(self):
        """
        Same as :any:`url`. Returns .png URL of bots/users avatar.

        :return: :class:`str`
            URL of the .png avatar image.
        """
        return self.base_url + '.png'

    @property
    def gif(self):
        """
        Returns .gif URL of bots/users avatar. IF user does not have animated avatar
        this method will produce URL that will get 404 error.

        :return: :class:`str`
            URL of the .gif avatar animation.
        """
        return self.base_url + '.gif'

    def size(self, size: int):
        """
        Returns URL of the resized static avatar image as specified.

        :param size: :class:`int`
            Size of the image in pixels. Min 16, max 2048.
        :return: :class:`str`
            URL of the resized image.
        """
        return self.base_url + f".png?size={size}"


class Description:
    __doc__ = "\n    Represents bot's description. By default returns short description, because long description is not required\n    and can be blank.\n\n    Attributes\n    -------------\n    short: :class:`str`\n        Short description\n    long: :class:`str`\n        Long description\n\n    "

    def __init__(self, short, long):
        self.short = short
        self.long = long

    def __get__(self, instance, owner):
        """
        If :class:`Description` accessed returns short description.

        :return: :class:`str`
            Short descriptions
        """
        return self.short

    def __str__(self):
        """
        If :class:`Description` accessed as string returns short description.

        :return: :class:`str`
            Short descriptions
        """
        return self.short


class DBLStats:
    __doc__ = '\n    Represents statistics object of a discord bot.\n\n    Attributes\n    -------------\n    server_count: :class:`str`\n        Returns server count.\n    shard_count: :class:`str`\n        Returns shard count.\n    shards: :class:`list`\n        Returns list of shards.\n\n    '

    def __init__(self, data):
        self.server_count = data.get('server_count', 'N/A')
        self.shard_count = data.get('shard_count', 'N/A')
        self.shards = data.get('shards', [])


class DBLBot:
    __doc__ = "\n    Represents DBL bot object.\n\n    Attributes\n    ----------\n    id: :class:`int`\n        Bot Client ID\n    username: :class:`str`\n        Bot's username\n    discriminator: :class:`int`\n        Bot's discriminator\n    username_full: :class:`str`\n        Full bot's username. Username#1234\n    mention: :class:`str`\n        Discord mention.\n    avatar: :class:`Avatar`\n        Returns :class:`Avatar` object.\n    library: :class:`str`\n        Bot's library\n    prefix: :class:`str`\n        Bot's prefix\n    description: :class:`Description`\n        Returns :class:`Description` object.\n    tags: :class:`list`\n        Returns list of tags\n    owners: :class:`list`\n        Returns list of owners\n    approved_date: :class:`datetime.Datetime`\n        Returns :class:`Datetime` object.\n    is_certified: :class:`bool`\n        Boolean. True if bot is certified, False otherwise\n    votes: :class:`int`\n        Bot's vote count\n    website: :class:`str`\n        Bot's website\n    github: :class:`str`\n        Bot's GitHub page\n    link: :class:`str`\n        Bot's DBL link. Prefers vanity URL\n    invite: :class:`str`\n        Bot's invite link\n    support: :class:`str`\n        Bot's support server URL\n\n    "

    def __init__(self, snowflake: str, username: str, discriminator: str, def_avatar: str, lib: str, prefix: str, short_desc: str, tags: list, owners: list, date: str, certified: bool, votes: int, other, client):
        self._stats_got = False
        self._stats_obj = None
        self.client = client
        self.id = int(snowflake)
        self.username = username
        self.discriminator = int(discriminator)
        self.username_full = f"{self.username}#{self.discriminator}"
        self.mention = f"<@{self.id}>"
        self.avatar = Avatar(other.get('avatar', def_avatar), self.id)
        self.library = lib
        self.prefix = prefix
        self.description = Description(short_desc, other.get('long_desc', ''))
        self.tags = tags
        self.owners = owners
        self.approved_date = dateutil.parser.parse(date)
        self.is_certified = certified
        self.votes = votes
        self.website = other.get('website', '')
        self.github = other.get('github', '')
        self.link = f"https://discordbots.org/bot/{other.get('vanity', self.id)}"
        self.invite = other.get('invite', '')
        self.support = f"https://discord.gg/{other.get('support', '')}"

    @classmethod
    def parse(cls, resp, client):
        try:
            data = cls(resp['id'], resp['username'], resp['discriminator'], resp['defAvatar'], resp['lib'], resp['prefix'], resp['shortdesc'], resp['tags'], resp['owners'], resp['date'], resp['certifiedBot'], resp['points'], resp, client)
        except KeyError:
            raise WeirdResponse
        else:
            return data

    @property
    async def stats(self) -> DBLStats:
        """|coro|

        Gets bot's statistics from DBL.

        :return: :class:`DBLStats`
            Returns :class:`DBLStats` object.
        """
        if self._stats_got:
            if self._stats_obj:
                return self._stats_obj
        r = await self.client.http.get(self.client.router.bot_stats.format_url(self.id))
        obj = DBLStats(r)
        self._stats_got = True
        self._stats_obj = obj
        return obj
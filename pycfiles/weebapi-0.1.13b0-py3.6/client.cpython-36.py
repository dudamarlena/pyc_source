# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\weebapi\client.py
# Compiled at: 2018-05-06 15:23:17
# Size of source mod 2**32: 11865 bytes
import asyncio, logging
from .data_objects import *
from .errors import *
from .img_gen import ImgGen
from .request_lib import krequest
from .router import Router
BASE_URL = 'https://api.weeb.sh/'
BASE_URL_V2 = 'https://api-v2.weeb.sh/'
logger = logging.getLogger()

class Client:
    __doc__ = '\n    .. _aiohttp session: https://aiohttp.readthedocs.io/en/stable/client_reference.html#client-session\n\n    Client object for Weeb.sh V2\n\n    This is a client object for Weeb.sh API. Here are two versions. Basic without discord.py bot\n    and a pluggable version that inserts this client object directly into your discord.py bot.\n\n\n    Represents a client connection that connects to weeb.sh. It works in two modes:\n        1. As a standalone variable.\n        2. Plugged-in to discord.py Bot or AutoShardedBot, see :any:`Client.pluggable`\n\n    Parameters\n    -------------\n    api_key: :class:`str`\n        Your weeb.sh api token.\n    wolke_token: bool[Optional]\n        *Not required.*\n        Is the api token type Wolke or Bearer.\n        **Default:** True\n    v2_api: bool[Optional]\n        *Not required.*\n        Use v2 API.\n        **Default:** False\n    **base_url: str[Optional]\n        *Not required.*\n        Specify different DBL API url.\n    **base_url: str[Optional]\n        *Not required.*\n        Specify different base url.\n    **bot: Bot or AutoShardedBot\n        Your bot client from discord.py\n    **loop: asyncio loop\n        Your asyncio loop.\n\n    '

    def __init__(self, api_key: str, wolke_token: bool=True, v2_api: bool=False, base_url: str=BASE_URL, bot=None, loop=asyncio.get_event_loop()):
        if v2_api is True:
            base_url = BASE_URL_V2
        self.api_key = api_key
        self._loop = loop
        self.route = Router(base_url)
        self.request = krequest(global_headers=[
         (
          'Authorization', f"Wolke {self.api_key}" if wolke_token else f"Bearer {self.api_key}")],
          loop=(self._loop))
        self.bot = bot
        self.img_gen = ImgGen(self)
        logger_string = str('Wolke ' if wolke_token else 'Bearer ') + self.api_key[-4:].rjust(len(self.api_key), '*')
        logger.info(f"WEEB.SH Logging in as {logger_string}")

    @classmethod
    def pluggable(cls, bot, api_key: str, *args, **kwargs):
        """
        Pluggable version of Client. Inserts Client directly into your Bot client.
        Called by using `bot.dbl`

        Parameters
        -------------
        bot: discord.ext.commands.Bot or discord.ext.commands.AutoShardedBot
            Your bot client from discord.py
        api_key: :class:`str`
            Your weeb.sh api token.

        .. note::
            Takes the same parameters as :class:`Client` class.
            Usage changes to ``bot.weebsh``. (``bot`` is your bot client variable)

        """
        try:
            return bot.weebsh
        except AttributeError:
            bot.weebsh = cls(api_key, *args, bot=bot, **kwargs)
            return bot.weebsh

    async def get_image(self, image: str or Image) -> Image:
        """|coro|

        This function gets image by it's ID.

        Parameters
        ------------
        image: :class:`str` or :class:`weebapi.data_objects.Image`
            Image ID from string or :class:`weebapi.data_objects.Image` object.

        :return: :class:`weebapi.data_objects.Image`

        """
        if isinstance(image, Image):
            image = image.snowflake
        else:
            if isinstance(image, str):
                pass
            else:
                raise ValueError
        g = await self.request.get(self.route.image.format_url(image))
        return Image.parse(g, self)

    async def get_preview(self, type_name: str, hidden: bool=False, nsfw: int=1) -> Preview:
        """|coro|

        This function gets a preview of the specified image type.

        .. container:: NSFW (not safe for work) Options

            .. describe:: 1 (Default)

                If the value of the nsfw parameter is ``1``, content with nsfw will be hidden.

            .. describe:: 2

                If the value of the nsfw parameter is ``2``, both nsfw and non-nsfw content will be shown.

            .. describe:: 3

                If the vaule of the nsfw parameter is ``3``, only content marked with nsfw will be shown.

        Parameters
        -----------
        type_name: :class:`str`
            Name of the image type for which you want the preview.
        **hidden: :class:`bool`
            Search in hidden image types. Defaults to False.
        **nsfw: :class:`int`
            Display options for NSFW content. Look for the valid values in the box above.

        :return: :class:`weebapi.data_objects.Preview`

        """
        params = {'preview': 'true'}
        if 1 <= nsfw <= 3:
            if nsfw == 1:
                nsfw = 'false'
            else:
                if nsfw == 2:
                    nsfw = 'true'
                else:
                    nsfw = 'only'
            params.update({'nsfw': nsfw})
        if hidden:
            params.update({'hidden': 'true'})
        g = await self.request.get((str(self.route.types)), params=params)
        status = int(g.get('status', 200))
        if status != 200:
            if status != 403:
                raise NotFound('This resource does not exist or you are not allowed to access.')
        if status == 403:
            raise Forbidden
        for p in g['preview']:
            if p['type'] == type_name:
                return Preview.parse(p, self)

        raise NotFound('Preview does not exist.')

    async def get_types(self, hidden: bool=False, nsfw: int=1) -> list:
        """|coro|

        This function gets the list of all available image types.

        .. container:: NSFW (not safe for work) Options

            .. describe:: 1 (Default)

                If the value of the nsfw parameter is ``1``, content with nsfw will be hidden.

            .. describe:: 2

                If the value of the nsfw parameter is ``2``, both nsfw and non-nsfw content will be shown.

            .. describe:: 3

                If the vaule of the nsfw parameter is ``3``, only content marked with nsfw will be shown.

        Parameters
        -----------
        **hidden: :class:`bool`
            Get hidden image types. Defaults to False.
        **nsfw: :class:`int`
            Display options for NSFW content. Look for the valid values in the box above.

        :return: Returns the list of :class:`weebapi.data_objects.ImageType` objects.

        """
        params = {}
        if 1 <= nsfw <= 3:
            if nsfw == 1:
                nsfw = 'false'
            else:
                if nsfw == 2:
                    nsfw = 'true'
                else:
                    nsfw = 'only'
            params.update({'nsfw': nsfw})
        if hidden:
            params.update({'hidden': 'true'})
        g = await self.request.get((str(self.route.types)), params=params)
        status = int(g.get('status', 200))
        if status != 200:
            if status != 403:
                raise NotFound('This resource does not exist or you are not allowed to access.')
        if status == 403:
            raise Forbidden
        return [ImageType(t, self) for t in g['types']]

    async def get_tags(self, hidden: bool=False, nsfw: int=1) -> list:
        """|coro|

        This function gets the list of all available image tags.

        .. container:: NSFW (not safe for work) Options

            .. describe:: 1 (Default)

                If the value of the nsfw parameter is ``1``, content with nsfw will be hidden.

            .. describe:: 2

                If the value of the nsfw parameter is ``2``, both nsfw and non-nsfw content will be shown.

            .. describe:: 3

                If the vaule of the nsfw parameter is ``3``, only content marked with nsfw will be shown.

        Parameters
        -----------
        **hidden: :class:`bool`
            Get hidden image tags. Defaults to False.
        **nsfw: :class:`int`
            Display options for NSFW content. Look for the valid values in the box above.

        :return: Returns the list of :class:`weebapi.data_objects.Tag` objects.

        """
        params = {}
        if 1 <= nsfw <= 3:
            if nsfw == 1:
                nsfw = 'false'
            else:
                if nsfw == 2:
                    nsfw = 'true'
                else:
                    nsfw = 'only'
            params.update({'nsfw': nsfw})
        if hidden:
            params.update({'hidden': 'true'})
        g = await self.request.get((str(self.route.tags)), params=params)
        status = int(g.get('status', 200))
        if status != 200:
            if status != 403:
                raise NotFound('This resource does not exist or you are not allowed to access.')
        if status == 403:
            raise Forbidden
        return [Tag(t, self) for t in g['tags']]

    async def get_random(self, tags: str or list=None, image_type: str=None, nsfw: int=1, hidden: bool=False, file_type: str=None) -> Image:
        """|coro|

        This function gets a random image of the specified tags or the image type.

        .. note::
            Make sure you either use comma separated or list of tags and/or one image type. You cannot
            leave both ``tags`` nor ``image_type`` variable blank, one of them must be used.

        .. container:: NSFW (not safe for work) Options

            .. describe:: 1 (Default)

                If the value of the nsfw parameter is ``1``, content with nsfw will be hidden.

            .. describe:: 2

                If the value of the nsfw parameter is ``2``, both nsfw and non-nsfw content will be shown.

            .. describe:: 3

                If the vaule of the nsfw parameter is ``3``, only content marked with nsfw will be shown.

        Parameters
        -----------
        **tags: :class:`str` or :class:`list`
            One tag or comma separated tags or list of image tags.
        **image_type: :class:`str`
            Specify image type.
        **hidden: :class:`bool`
            Get hidden image tags. Defaults to False.
        **nsfw: :class:`int`
            Display options for NSFW content. Look for the valid values in the box above.
        **file_type: :class:`str`
            One of ``jpg, jpeg, png, gif`` file types.

        :return: Returns the :class:`weebapi.data_objects.Image` object.
        """
        params = {}
        if tags:
            if isinstance(tags, str):
                params.update({'tags': tags})
            elif isinstance(tags, list):
                params.update({'tags': ','.join(tags)})
        if image_type:
            params.update({'type': image_type})
        else:
            if not params:
                raise MissingRequiredArguments('Add tags and/or type.')
            if 1 <= nsfw <= 3:
                if nsfw == 1:
                    nsfw = 'false'
                else:
                    if nsfw == 2:
                        nsfw = 'true'
                    else:
                        nsfw = 'only'
                params.update({'nsfw': nsfw})
            else:
                raise ValueError('Must be >=1 and <=3!')
        if hidden:
            params.update({'hidden': 'true'})
        if file_type:
            if file_type in ('jpg', 'jpeg', 'png', 'gif'):
                params.update({'filetype': file_type})
            else:
                raise ValueError('Invalid filetype. (Available: jpg, jpeg, png, gif)')
        g = await self.request.get((str(self.route.random)), params=params)
        return Image.parse(g, self)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nsfw_dl/loaders/gelbooru.py
# Compiled at: 2017-09-19 09:41:52
# Size of source mod 2**32: 922 bytes
"""
Read the license at:
https://github.com/IzunaDevs/nsfw_dl/blob/master/LICENSE
"""
from nsfw_dl.bases import BaseSearchHTML

class GelbooruRandom:
    __doc__ = ' Gets a random image from gelbooru. '
    data_format = 'bs4/html'

    @staticmethod
    def prepare_url(args):
        """ .... """
        type(args)
        return ('https://www.gelbooru.com/index.php?page=post&s=random', {}, {})

    @staticmethod
    def get_image(data):
        """ .... """
        try:
            return f"https:{data.find(id='image').get('src')}"
        except AttributeError:
            raise AttributeError(str(data))


class GelbooruSearch(BaseSearchHTML):
    __doc__ = ' Gets a random image with a specific tag from gelbooru. '
    data_format = 'bs4/html'

    @staticmethod
    def prepare_url(args):
        """ .... """
        return (
         f"https://www.gelbooru.com/index.php?page=post&s=list&tags={args}", {}, {})
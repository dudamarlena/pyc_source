# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nsfw_dl/loaders/lolibooru.py
# Compiled at: 2017-09-19 09:41:52
# Size of source mod 2**32: 765 bytes
"""
Read the license at:
https://github.com/IzunaDevs/nsfw_dl/blob/master/LICENSE
"""
from nsfw_dl.bases import BaseSearchJSON

class LolibooruRandom:
    __doc__ = ' Gets a random image from lolibooru. '
    data_format = 'bs4/html'

    @staticmethod
    def prepare_url(args):
        """ ... """
        type(args)
        return ('https://lolibooru.moe/post/random/', {}, {})

    @staticmethod
    def get_image(data):
        """ ... """
        return data.find(id='highres').get('href')


class LolibooruSearch(BaseSearchJSON):
    __doc__ = ' Gets a random image with a specific tag from lolibooru. '
    data_format = 'json'

    @staticmethod
    def prepare_url(args):
        """ ... """
        return (
         f"https://lolibooru.moe/post/index.json?tags={args}", {}, {})
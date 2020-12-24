# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nsfw_dl/bases.py
# Compiled at: 2017-09-19 09:41:52
# Size of source mod 2**32: 1316 bytes
"""
Read the license at:
https://github.com/IzunaDevs/nsfw_dl/blob/master/LICENSE
"""
import random
from nsfw_dl.errors import NoResultsFound

class BaseSearchXML:
    __doc__ = ' base xml search class. '

    @staticmethod
    def prepare_url(args):
        """ ... """
        pass

    @staticmethod
    def get_image(data):
        """ ... """
        if data:
            if int(data.find('posts')['count']) > 0:
                imagelist = [tag.get('file_url') for tag in data.find_all('post')]
                return random.choice(imagelist)
        raise NoResultsFound


class BaseSearchHTML:
    __doc__ = ' base html search class. '

    @staticmethod
    def prepare_url(args):
        """ ... """
        pass

    @staticmethod
    def get_image(data):
        """ ... """
        if data:
            images = data.find_all(attrs='thumb')
            if images:
                return random.choice(images).find('img').get('src')
        raise NoResultsFound


class BaseSearchJSON:
    __doc__ = ' base json search class. '

    @staticmethod
    def prepare_url(args):
        """ ... """
        pass

    @staticmethod
    def get_image(data):
        """ ... """
        if data:
            return random.choice(data)['file_url']
        raise NoResultsFound
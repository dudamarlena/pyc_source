# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nsfw_dl/loaders/tbib.py
# Compiled at: 2017-09-19 09:41:52
# Size of source mod 2**32: 808 bytes
"""
Read the license at:
https://github.com/IzunaDevs/nsfw_dl/blob/master/LICENSE
"""
from nsfw_dl.bases import BaseSearchXML

class TbibRandom:
    __doc__ = ' Gets a random image from tbib. '
    data_format = 'bs4/html'

    @staticmethod
    def prepare_url(args):
        """ ... """
        type(args)
        return ('https://www.tbib.org/index.php?page=post&s=random', {}, {})

    @staticmethod
    def get_image(data):
        """ ... """
        return f"https:{data.find(id='image').get('src')}"


class TbibSearch(BaseSearchXML):
    __doc__ = ' Gets a random image with a specific tag from tbib. '
    data_format = 'bs4/xml'

    @staticmethod
    def prepare_url(args):
        """ ... """
        return (
         f"https://www.tbib.org/index.php?page=dapi&s=post&q=index&tags={args}", {}, {})
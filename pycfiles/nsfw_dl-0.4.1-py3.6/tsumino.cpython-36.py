# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nsfw_dl/loaders/tsumino.py
# Compiled at: 2017-09-19 09:41:52
# Size of source mod 2**32: 441 bytes
"""
Read the license at:
https://github.com/IzunaDevs/nsfw_dl/blob/master/LICENSE
"""

class TsuminoRandom:
    __doc__ = ' Gets a random image from tsumino. '
    data_format = 'url'

    @staticmethod
    def prepare_url(args):
        """ ... """
        type(args)
        return ('http://www.tsumino.com/Browse/Random', {}, {})

    @staticmethod
    def get_image(data):
        """ ... """
        return data.find(id='highres').get('href')
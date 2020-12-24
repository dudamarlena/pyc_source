# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nsfw_dl/errors.py
# Compiled at: 2017-09-19 09:41:52
# Size of source mod 2**32: 627 bytes
"""
Read the license at:
https://github.com/IzunaDevs/nsfw_dl/blob/master/LICENSE
"""
__all__ = [
 'NoLoader', 'NoResultsFound', 'NoXMLParser',
 'UnsupportedDataFormat']

class NoLoader(Exception):
    __doc__ = '\n    Thrown when there is no such loader in the NSFWDL instance\n    '


class NoResultsFound(Exception):
    __doc__ = '\n    Thrown when the search found no results for the search.\n    '


class NoXMLParser(Exception):
    __doc__ = '\n    Thrown when there is no xml parser.\n    '


class UnsupportedDataFormat(Exception):
    __doc__ = '\n    Thrown when there is an unsupported format.\n    '
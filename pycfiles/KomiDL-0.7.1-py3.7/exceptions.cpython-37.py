# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komidl\exceptions.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 1200 bytes
"""This module defines custom exceptions raised and caught by KomiDL"""

class ExtractorFailed(Exception):
    __doc__ = 'Any failures as a result of the extractor unable to handle an\n       appropriate URL\n\n    If the extractor returns an invalid URL for an image, then it is\n    considered to be an ExtractorFailed exception, and not an InvalidURL\n    exception.\n    '


class InvalidURL(Exception):
    __doc__ = 'Any inappropriate URL given by the user returned by the server'
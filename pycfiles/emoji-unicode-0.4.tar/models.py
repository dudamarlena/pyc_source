# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esteban/PycharmProjects/emoji-awesome/emoji_unicode/models.py
# Compiled at: 2015-11-18 15:12:07
from __future__ import unicode_literals
from .utils import unicode_to_code_point
from .pattern import EMO_VARIATION, ZWJ
JOINER_CHARS = {
 EMO_VARIATION, ZWJ}

class Emoji(object):
    """
    Emoji is used in the process of :py:func:`.replace` unicode emojis in a text

    :param str unicode: Unicode emoji
    """

    def __init__(self, unicode):
        self.unicode = unicode

    @property
    def code_points(self):
        """
        Code points representing the unicode emoji,        the result is normalized as by :py:func:`.normalize`

        :return: Code points representing the emoji,        with no joiner chars and lower cased, ie: 1f3c3-1f3fc
        :rtype: str
        """
        return (b'-').join(unicode_to_code_point(u) for u in self.unicode if u not in JOINER_CHARS)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\tokens\number_token.py
# Compiled at: 2020-01-31 09:24:14
# Size of source mod 2**32: 1863 bytes
from miniworldmaker.tokens import text_token

class NumberToken(text_token.TextToken):
    __doc__ = '\n    A number token shows a Number.\n\n    You have to set the size of the token with self.size() manually so that\n    the complete text can be seen.\n\n    Args:\n        position: Top-Left position of Number\n        number: The initial number\n        font-size: The size of the font (default: 80)\n        color: The color of the font (default: white)\n\n    Examples:\n        >>> self.score = NumberToken(position = (0, 0), number=0)\n        Sets a new NumberToken to display the score.\n\n        >>> number = self.score.get_number()\n        Gets the number stored in the NumberToken\n\n        >>> self.score.set_number(3)\n        Sets the number stored in the NumberToken\n    '

    def __init__(self, position, number=0, font_size=80, color=(255, 255, 255, 255)):
        super().__init__(position, str(number), font_size, color)
        self.set_number(number)
        self.is_static = True

    def inc(self):
        """
        Increases the number by one
        """
        self.number += 1
        self.set_text(str(self.number))

    def set_number(self, number):
        """
        Sets the number

        Args:
            number: The number which should be displayed

        Examples:
            >>> self.number_token.set_number(3)
            Sets the number stored in the NumberToken
        """
        self.number = number
        self.set_text(str(self.number))

    def get_number(self) -> int:
        """

        Returns:
            The current number

        Examples:
            >>> number = self.number_token.get_number()
            Gets the number stored in the NumberToken
        """
        self.costume.call_action('text changed')
        return int(self.costume.text)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thelatinlibrary/tools.py
# Compiled at: 2019-01-13 09:19:26
# Size of source mod 2**32: 1977 bytes
import re
from html import unescape
roman_numerals = re.compile('\\b(?=[MDCLXVI]+\\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\\b', re.IGNORECASE)

def titleize(title: str):
    """
    Format a title including roman numerals.

    Args:
      title (str): The string you want to format.

    Example:
        >>> from thelatinlibrary.tools import titleize
        >>> titleize("de bello gallico")
        'De Bello Gallico'
        >>> titleize("liber i")
        'Liber I'
        >>> titleize("liber ii")
        'Liber II'
        >>> titleize("liber lvxig")
        'Liber Lvxig'

    Returns:
      str: The formatted title.
    """
    return roman_numerals.sub(lambda number: number.group().upper(), unescape(title.title().strip().rstrip()))
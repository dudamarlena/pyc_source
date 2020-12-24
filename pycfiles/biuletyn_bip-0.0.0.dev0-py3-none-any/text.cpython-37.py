# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/utils/text.py
# Compiled at: 2019-09-28 15:02:04
# Size of source mod 2**32: 571 bytes


def yesno(value: bool, capitalize: bool=True) -> str:
    """Return "yes" or "no" as textual representation of Boolean value.
    Returned string is capitalized by default.

    :param value: value to be represented as `str`
    :type value: bool
    :param capitalize: whether to capitalize output string, defaults to True
    :type capitalize: bool, optional
    :return: textual representation of Boolean value
    :rtype: str
    """
    if value:
        ret = 'tak'
    else:
        ret = 'nie'
    if capitalize:
        return ret.capitalize()
    return ret
# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/powerline/output.py
# Compiled at: 2008-04-11 15:13:57
__doc__ = 'Output and formatting functions.\n\nFunctions\n=========\n\nordinalize and join are both for string formatting. Both currently only work with English, unfortunately.\n'

def ordinalize(num):
    """Transforms a number into its ordinal equivalent.

        >>> ordinalize(1), ordinalize(2), ordinalize(3), ordinalize(4)
        ('1st', '2nd', '3rd', '4th')
        >>> ordinalize(11), ordinalize(21), ordinalize(50002)
        ('11th', '21st', '50002nd')
        """
    special_suffixes = {'1': 'st', '2': 'nd', '3': 'rd'}
    default_return = 'th'
    digits = str(abs(num))
    last_digit = digits[-1:]
    if last_digit in special_suffixes.keys():
        if len(digits) == 1 or digits[(-2)] != '1':
            default_return = special_suffixes[last_digit]
    return str(num) + default_return


def join(list_, conjunction='or'):
    """Joins a list together in a readable form.

        >>> join(['a', 'b', 'c'])
        'a, b or c'
        >>> join(['a', 'b'])
        'a or b'
        >>> join(['a', 'b', 'c'], 'and')
        'a, b and c'
        >>> join(['a'])
        'a'
        >>> join([])
        ''
        """
    if len(list_) == 0:
        return ''
    elif len(list_) == 1:
        return str(list_[0])
    elif len(list_) == 2:
        return (' %s ' % conjunction).join(list_)
    else:
        return (', ').join(list_[:-1]) + ' %s ' % conjunction + list_[(-1)]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/g/projects/superhelp/build/lib/superhelp/utils.py
# Compiled at: 2020-04-11 04:02:40
# Size of source mod 2**32: 1530 bytes
from textwrap import dedent
from . import conf

def get_nice_str_list(items, *, quoter='`'):
    """
    Get a nice English phrase listing the items.

    :param sequence items: individual items to put into a phrase.
    :param str quoter: default is backtick because it is expected that the most
     common items will be names (variables).
    :return: nice phrase
    :rtype: str
    """
    nice_str_list = ', '.join([f"{quoter}{item}{quoter}" for item in items[:-1]])
    if nice_str_list:
        nice_str_list += ' and '
    nice_str_list += f"{quoter}{items[(-1)]}{quoter}"
    return nice_str_list


def int2nice(num):
    """
    :return: nicer version of number ready for use in sentences
    :rtype: str
    """
    nice = {0:'no', 
     1:'one', 
     2:'two', 
     3:'three', 
     4:'four', 
     5:'five', 
     6:'six', 
     7:'seven', 
     8:'eight', 
     9:'nine', 
     10:'ten', 
     11:'twelve', 
     12:'twelve'}
    return nice.get(num, num)


def layout_comment(raw_comment, *, is_code=False):
    if is_code:
        lines = [
         conf.PYTHON_CODE_START] + dedent(raw_comment).split('\n') + [conf.PYTHON_CODE_END]
        indented_lines = [f"{'    '}{line}" for line in lines]
        comment = '\n'.join(indented_lines) + '\n'
    else:
        comment = dedent(raw_comment)
    return comment
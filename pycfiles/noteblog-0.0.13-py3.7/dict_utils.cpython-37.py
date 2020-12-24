# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/data/dict_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 1710 bytes
"""
@author = super_fazai
@File    : dict_utils.py
@connect : superonesfazai@gmail.com
"""
__all__ = [
 'dict_obj_2_markdown_table']

def dict_obj_2_markdown_table(target) -> str:
    """
    字典对象转换为markdown table
        eg: 
            data = [
                {
                    'pr': 291,
                    'status': 'closed',
                    'date': 'None',
                    'title': 'Adds new wiz bang feature'
                },
                {
                    'pr': 290,
                    'status': 'v1.0',
                    'date': 'None',
                    'title': 'Updates UI to be more awesome'
                }
            ]
            print(dict_obj_2_markdown_table(data))
            # | pr | status | date | title |
            # |-----|-----|-----|-----|
            # | 291 | closed | None | Adds new wiz bang feature |
            # | 290 | v1.0 | None | Updates UI to be more awesome |
    :param target: 
    :return: 
    """
    markdown_table = ''
    markdown_header = '| ' + ' | '.join(map(str, target[0].keys())) + ' |'
    markdown_header_separator = '|-----' * len(target[0].keys()) + '|'
    markdown_table += markdown_header + '\n'
    markdown_table += markdown_header_separator + '\n'
    for row in target:
        markdown_row = ''
        for key, col in row.items():
            markdown_row += '| ' + str(col) + ' '

        markdown_table += markdown_row + '|' + '\n'

    return markdown_table
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/utils/pagination.py
# Compiled at: 2020-02-08 07:33:40
# Size of source mod 2**32: 588 bytes


def paginate(l, context):
    """
    yields: page, page_index, total_pages

    """
    DEFAULT_PAGINATION = getattr(context.settings, 'DEFAULT_PAGINATION')
    l_count = len(l)
    if l_count > DEFAULT_PAGINATION:
        total_pages = (l_count - l_count % DEFAULT_PAGINATION) // DEFAULT_PAGINATION + int(l_count % DEFAULT_PAGINATION > 0)
    else:
        total_pages = 1
    for index in range(total_pages):
        yield (l[index * DEFAULT_PAGINATION:(index + 1) * DEFAULT_PAGINATION],
         index + 1,
         total_pages)
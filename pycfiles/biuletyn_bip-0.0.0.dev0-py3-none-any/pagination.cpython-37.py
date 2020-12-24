# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/utils/pagination.py
# Compiled at: 2019-09-28 14:47:55
# Size of source mod 2**32: 519 bytes
from flask import request, url_for, current_app

def url_for_other_page(page):
    args = request.view_args.copy()
    args['p'] = page
    return url_for((request.endpoint), **args)


def get_page(arg_name='p'):
    try:
        return int(request.args.get(arg_name, '1'))
    except ValueError:
        return 1


def paginate(query, page=None, size=None):
    if page is None:
        page = get_page()
    if size is None:
        size = current_app.config.get('LIST_SIZE', 20)
    return query.paginate(page, size)
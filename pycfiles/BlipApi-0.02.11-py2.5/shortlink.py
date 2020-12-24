# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/shortlink.py
# Compiled at: 2010-12-26 11:28:50
from _utils import encode_multipart

def create(**args):
    """ Create new shortened link. """
    if not args.get('link'):
        raise ValueError('Url is missing.')
    url = '/shortlinks'
    fields = {'shortlink[original_link]': args['link']}
    (data, boundary) = encode_multipart(fields)
    return dict(url=url, method='post', data=data, boundary=boundary)


def read(**args):
    """ Get list of shortlinks, or info about specified shortlink (by it's code). """
    if args.get('code'):
        url = '/shortlinks/' + args['code']
    elif args.get('since_id'):
        url = '/shortlinks/' + str(args['since_id']) + '/all_since'
    else:
        url = '/shortlinks/all'
    params = dict()
    params['limit'] = args.get('limit', 10)
    params['offset'] = args.get('offset', 0)
    return dict(url=url, method='get', params=params)
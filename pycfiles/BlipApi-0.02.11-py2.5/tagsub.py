# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/tagsub.py
# Compiled at: 2010-12-26 11:28:50
import os.path, re
from _utils import encode_multipart

def _validate_tag_name(tag):
    return re.match('^[-a-zA-Z0-9_ĄąĆćĘęŁłŃńÓóŚśŻżŹź]+$', tag)


def create(**args):
    if not args.get('name') or not _validate_tag_name(args['name']):
        raise ValueError('Incorrect tag name or tag name missing.')
    if args.setdefault('type', 'subscribe') not in ('all', 'ignore', 'subscribe'):
        raise ValueError('Incorrect value for "type" argument. Should be one of: ignore, subscribe.')
    if args['type'] == 'all':
        raise ValueError('For creating, "all" type is incorrect. Should be one of: "ignore", "subscribe".')
    return dict(url='/tag_subscriptions/%s/%s' % (args['type'], args['name']), method='put')


def read(**args):
    if args.setdefault('type', 'subscribe') not in ('all', 'ignore', 'subscribe'):
        raise ValueError('Incorrect value for "type" argument. Should be one of: ignore, subscribe.')
    if args['type'] != 'all':
        url = '/tag_subscriptions/' + args['type'] + 'd'
    else:
        url = '/tag_subscriptions'
    params = dict()
    params['include'] = (',').join(args.get('include', ''))
    return dict(url=url, method='get', params=params)


def delete(**args):
    if not args.get('name') or not _validate_tag_name(args['name']):
        raise ValueError('Incorrect tag name or tag name missing.')
    return dict(url='/tag_subscriptions/tracked/' + args['name'], method='put')
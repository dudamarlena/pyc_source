# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/update.py
# Compiled at: 2010-12-26 11:28:50
import os.path
from _utils import encode_multipart

def create(**args):
    """ Create new update. """
    if not args.get('body'):
        raise ValueError('Update body is missing.')
    if args.get('user'):
        if args.get('private'):
            args['private'] = '>'
        else:
            args['private'] = ''
        args['body'] = '>%s%s %s' % (args['private'], args['user'], args['body'])
    fields = {'update[body]': args['body']}
    if args.get('image') and os.path.isfile(args['image']):
        fields['update[picture]'] = (
         args['image'], args['image'])
    (data, boundary) = encode_multipart(fields)
    return dict(url='/updates', method='post', data=data, boundary=boundary)


def read(**args):
    """ Read updates. """
    if args.get('user'):
        if args['user'] == '__ALL__':
            if args.get('since_id'):
                url = '/updates/' + str(args['since_id']) + '/all_since'
            else:
                url = '/updates/all'
        elif args.get('since_id'):
            url = '/users/' + args['user'] + '/updates/' + str(args['since_id']) + '/since'
        else:
            url = '/users/' + args['user'] + '/updates'
    elif args.get('id'):
        url = '/updates/' + str(args['id'])
    else:
        url = '/updates'
        if args.get('since_id'):
            url += '/' + str(args['since_id']) + '/since'
    params = dict()
    params['limit'] = args.get('limit', 10)
    params['offset'] = args.get('offset', 0)
    params['include'] = (',').join(args.get('include', ''))
    return dict(url=url, method='get', params=params)


def delete(**args):
    """ Delete update. """
    if not args.get('id'):
        raise ValueError('Update ID is missing.')
    return dict(url='/updates/' + str(args['id']), method='delete')
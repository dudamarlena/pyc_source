# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/privmsg.py
# Compiled at: 2010-12-26 11:28:50
import os.path
from _utils import encode_multipart

def create(**args):
    """ Create new private message. """
    if not args.get('body') or not args.get('user'):
        raise ValueError('Private_message body or recipient is missing.')
    fields = {'private_message[body]': args['body'], 
       'private_message[recipient]': args['user']}
    if args.get('image') and os.path.isfile(args['image']):
        fields['private_message[picture]'] = (
         args['image'], args['image'])
    (data, boundary) = encode_multipart(fields)
    return dict(url='/private_messages', method='post', data=data, boundary=boundary)


def read(**args):
    """ Read user's private messages. """
    if args.get('since_id'):
        url = '/private_messages/since/' + str(args['since_id'])
    elif args.get('id'):
        url = '/private_messages/' + str(args['id'])
    else:
        url = '/private_messages'
    params = dict()
    params['limit'] = args.get('limit', 10)
    params['offset'] = args.get('offset', 0)
    params['include'] = (',').join(args.get('include', ''))
    return dict(url=url, method='get', params=params)


def delete(**args):
    """ Delete specified private message. """
    if not args.get('id'):
        raise ValueError('Private_message ID is missing.')
    return dict(url='/private_messages/' + str(args['id']), method='delete')
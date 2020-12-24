# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/avatar.py
# Compiled at: 2010-12-26 11:28:50
import os.path
from _utils import encode_multipart

def read(**args):
    """ Get info about specified user's avatar. """
    if not args.get('user'):
        url = '/avatar'
    elif args.get('url_only'):
        size = args.get('size', 'standard')
        if size not in ('femto', 'nano', 'pico', 'standard', 'large'):
            raise ValueError('Unrecognized size of avatar')
        return dict(just_return='http://blip.pl/users/' + args.get('user') + '/avatar/' + size + '.jpg')
    else:
        url = '/users/' + args['user'] + '/avatar'
    return dict(url=url, method='get')


def update(**args):
    """ Update current user avatar. """
    if not args.get('image') or not os.path.isfile(args['image']):
        raise ValueError('Avatar path missing or file not found.')
    (data, boundary) = encode_multipart({'avatar[file]': (args['image'], args['image'])})
    return dict(url='/avatar', method='post', boundary=boundary, data=data)


def delete():
    """ Delete current user avatar. """
    return dict(url='/avatar', method='delete')
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/background.py
# Compiled at: 2010-12-26 11:28:50
import os.path
from _utils import encode_multipart

def read(**args):
    """ Get specified user's background info. """
    if not args.get('user'):
        url = '/background'
    else:
        url = '/users/' + args['user'] + '/background'
    return dict(url='/users/' + args['user'] + '/background', method='get')


def update(**args):
    """ Update current user background. """
    if not args.get('image') or not os.path.isfile(args['image']):
        raise ValueError('Background path is missing or file not found.')
    (data, boundary) = encode_multipart({'background[file]': (args['image'], args['image'])})
    return dict(url='/background', method='post', boundary=boundary, data=data)


def delete():
    """ Delete current user background. """
    return dict(url='/background', method='delete')
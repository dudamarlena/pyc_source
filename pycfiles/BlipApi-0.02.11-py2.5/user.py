# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/user.py
# Compiled at: 2010-12-26 11:28:50


def read(**args):
    """ Get info about user. """
    if args.get('user'):
        url = '/users/' + args['user']
    else:
        url = '/profile'
    params = dict()
    params['include'] = (',').join(args.get('include', ''))
    return dict(url=url, method='get', params=params)
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/notice.py
# Compiled at: 2010-12-26 11:28:50


def read(**args):
    """ Get notices. """
    if args.get('user'):
        if args['user'] == '__ALL__':
            if args.get('since_id'):
                url = '/notices/' + str(args['since_id']) + '/all_since'
            else:
                url = '/notices/all'
        elif args.get('since_id'):
            url = '/users/' + args['user'] + '/notices/' + str(args['since_id']) + '/since'
        else:
            url = '/users/' + args['user'] + '/notices'
    elif args.get('id'):
        url = '/notices/' + str(args['id'])
    else:
        url = '/notices'
        if args.get('since_id'):
            url += '/since/' + str(args['since_id'])
    params = dict()
    params['limit'] = args.get('limit', 10)
    params['offset'] = args.get('offset', 0)
    params['include'] = (',').join(args.get('include', ''))
    return dict(url=url, method='get', params=params)
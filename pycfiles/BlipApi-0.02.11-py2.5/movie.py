# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/movie.py
# Compiled at: 2010-12-26 11:28:50


def read(**args):
    """ Read movie data from specified update. """
    if not args.get('id'):
        raise ValueError('Update ID is missing.')
    return dict(url='/updates/' + str(args['id']) + '/movie', method='get')
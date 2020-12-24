# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/gmg_commands/deletemedia.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 1710 bytes
from __future__ import print_function
import sys
from mediagoblin.gmg_commands import util as commands_util

def parser_setup(subparser):
    subparser.add_argument('media_ids', help='Comma separated list of media IDs will be deleted.')


def deletemedia(args):
    app = commands_util.setup_app(args)
    media_ids = set([int(mid) for mid in args.media_ids.split(',') if mid.isdigit()])
    if not media_ids:
        print("Can't find any valid media ID(s).")
        sys.exit(1)
    found_medias = set()
    filter_ids = app.db.MediaEntry.id.in_(media_ids)
    medias = app.db.MediaEntry.query.filter(filter_ids).all()
    for media in medias:
        found_medias.add(media.id)
        media.delete()
        print('Media ID %d has been deleted.' % media.id)

    for media in media_ids - found_medias:
        print("Can't find a media with ID %d." % media)

    print('Done.')
    sys.exit(0)
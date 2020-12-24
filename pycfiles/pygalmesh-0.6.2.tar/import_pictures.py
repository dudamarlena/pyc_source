# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyGallerid/scripts/import_pictures.py
# Compiled at: 2012-01-31 10:40:29
__doc__ = '\nScript for importing pictures into the pyGallerid database.\n'
import os, sys
from pyramid_zodbconn import db_from_uri
import transaction
from pyramid.paster import get_appsettings, setup_logging
from ..models import appmaker, retrieve_user, retrieve_gallery
from ..utils.picture import import_gallery_container

def usage(argv):
    cmd = os.path.basename(argv[0])
    print 'usage: %s <config_uri> <username> <path> <sorting_order>\n(example: "%s development.ini hepp new_pictures [text|number|date]' % (
     cmd, cmd)
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 4:
        usage(argv)
    config_uri = argv[1]
    username = argv[2]
    path = argv[3]
    sorting_order = 'number'
    if len(argv) > 4:
        sorting_order = argv[4]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    db = db_from_uri(settings['zodbconn.uri'])
    conn = db.open()
    zodb_root = conn.root()
    with transaction.manager:
        import_pictures(zodb_root, settings, username, path, sorting_order)
        transaction.commit()


def import_pictures(zodb_root, settings, username, path, sorting_order):
    app = appmaker(zodb_root)
    user = retrieve_user(app, username)
    gallery = retrieve_gallery(user)
    cwd = os.getcwd()
    os.chdir(path)
    container = import_gallery_container('.', settings, move_files=False, sorting_order=sorting_order)
    os.chdir(cwd)
    if container is not None:
        for child in container:
            gallery.add(child)

    return